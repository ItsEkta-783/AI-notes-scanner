import time
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

def create_pdf(summary, bullets):
    file_path = f"summary_{int(time.time())}.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # 🎨 Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        alignment=1,
        textColor=colors.HexColor("#ff4d88"),
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        textColor=colors.HexColor("#333333"),
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        spaceAfter=10,
        leading=15
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        leftIndent=10,
        spaceAfter=5
    )

    content = []

    # ✅ FIXED LOGO PATH
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_dir, "static", "ai_notes_scanner_logo.png")

        logo = Image(logo_path, width=60, height=60)
        logo.hAlign = 'CENTER'
        content.append(logo)
        content.append(Spacer(1, 10))
    except Exception as e:
        print("Logo not found:", e)

    # 🧠 Title
    content.append(Paragraph("NeuraNotes Summary ", title_style))

    # 📄 Summary
    content.append(Paragraph("Summary", heading_style))
    content.append(Paragraph(summary, normal_style))

    # 📌 Key Points
    content.append(Paragraph("Key Points", heading_style))
    for point in bullets:
        content.append(Paragraph(f"• {point}", bullet_style))

    doc.build(content)

    return file_path