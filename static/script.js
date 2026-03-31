function showFileName(input) {
    const file = input.files[0];
    if (!file) return;

    const fileName = document.getElementById("file-name");
    const previewImg = document.getElementById("preview-img");
    const pdfPreview = document.getElementById("pdf-preview");

    // Reset preview states
    previewImg.style.display = "none";
    pdfPreview.style.display = "none";
    fileName.innerText = "";

    let icon = "📄";

    // PDF preview
    if (file.type === "application/pdf") {
        icon = "📕";
        pdfPreview.style.display = "inline-block";
        pdfPreview.innerText = `${icon} ${file.name}`;
    }

    // Image preview
    else if (file.type.startsWith("image/")) {
        icon = "🖼️";

        const reader = new FileReader();
        reader.onload = function () {
            previewImg.src = reader.result;
            previewImg.style.display = "block";
        };
        reader.readAsDataURL(file);
    }

    // Set file name label (outside preview)
    fileName.innerText = `${icon} ${file.name}`;
    
    // Hide processing text until scan starts
    document.getElementById("loading-text").style.display = "none";
    document.getElementById("loading").style.display = "none";
}

function showLoading() {
    const fileInput = document.getElementById("fileInput");
    const spinner = document.getElementById("loading");
    const text = document.getElementById("loading-text");
    const btn = document.getElementById("scan-btn");

    // Prevent scanning without file
    if (!fileInput.files.length) {
        alert("Please upload a file first!");
        return false;
    }

    // Start spinner only
    spinner.style.display = "block";

    // Hide the static "Processing..." text, we don't want double indicators
    text.style.display = "none";

    // Disable button & update text
    btn.disabled = true;
    btn.innerText = "Processing...";

    return true;
}

function toggleDarkMode() {
    document.body.classList.toggle("dark");
}

function speakText(text) {
    let speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
}