from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
from ocr import extract_text
from summarizer import summarize_text , bullet_summary
import os , time
from pdf_generator import create_pdf
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.background import BackgroundTasks
from pdf2image import convert_from_path

latest_summary = ""
latest_bullets = []

history = []

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request ,"history": history })

from pdf2image import convert_from_path

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    
    if not file.filename:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "No file uploaded",
            "history": history
        })
    
    file_path = f"temp_{int(time.time())}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = ""

    # 🔥 HANDLE PDF
    if file.filename.lower().endswith(".pdf"):
        try:
            images = convert_from_path(file_path)

            for img in images:
                temp_img_path = f"temp_page_{int(time.time())}.png"
                img.save(temp_img_path, "PNG")

                extracted_text += extract_text(temp_img_path) + "\n"

                os.remove(temp_img_path)

        except Exception as e:
            os.remove(file_path)
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": "PDF processing failed",
                "history": history
            })

    # 🔥 HANDLE IMAGE
    else:
        extracted_text = extract_text(file_path)

    os.remove(file_path)

    summary = summarize_text(extracted_text)
    bullets = bullet_summary(extracted_text)

    global latest_summary, latest_bullets
    latest_summary = summary
    latest_bullets = bullets

    history.append({
        "summary": summary,
        "time": time.strftime("%H:%M:%S")
    })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "text": extracted_text,
        "summary": summary,
        "bullets": bullets,
        "history": history
    })

@app.get("/download")
def download_pdf(background_tasks: BackgroundTasks):
    file_path = create_pdf(latest_summary, latest_bullets)

    # delete file after response is sent
    background_tasks.add_task(os.remove, file_path)

    return FileResponse(
        file_path,
        media_type='application/pdf',
        filename="summary.pdf"
    )

app.mount("/static", StaticFiles(directory="static"), name="static")
