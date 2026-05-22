import os
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path

import pdfplumber
import pypdfium2 as pdfium
import pytesseract
from PIL import Image

from modules.config import MACOS_OCR_SCRIPT, TEMP_FOLDER, TESSERACT_PATH


def _resolve_tesseract_command():
    if TESSERACT_PATH and os.path.exists(TESSERACT_PATH):
        return TESSERACT_PATH

    detected = shutil.which("tesseract")
    return detected


TESSERACT_COMMAND = _resolve_tesseract_command()

if TESSERACT_COMMAND:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_COMMAND


def _tesseract_available():
    return bool(TESSERACT_COMMAND)


def _macos_ocr_available():
    return platform.system() == "Darwin" and MACOS_OCR_SCRIPT.exists()


def _extract_text_with_tesseract(image_path):
    image = Image.open(image_path)
    image = image.convert("L")
    image = image.point(lambda x: 0 if x < 140 else 255)
    return pytesseract.image_to_string(image)


def _extract_text_with_macos_ocr(image_path):
    module_cache_dir = TEMP_FOLDER / "swift-module-cache"
    module_cache_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["CLANG_MODULE_CACHE_PATH"] = str(module_cache_dir)
    env["SWIFT_MODULECACHE_PATH"] = str(module_cache_dir)

    result = subprocess.run(
        [
            "swift",
            "-module-cache-path",
            str(module_cache_dir),
            str(MACOS_OCR_SCRIPT),
            str(image_path)
        ],
        check=True,
        capture_output=True,
        text=True,
        env=env
    )
    return result.stdout


def _extract_text_from_image_file(image_path):
    if _tesseract_available():
        return _extract_text_with_tesseract(image_path)

    if _macos_ocr_available():
        return _extract_text_with_macos_ocr(image_path)

    raise RuntimeError(
        "OCR is unavailable on this machine. Install Tesseract or use macOS for built-in OCR support."
    )


def _extract_text_from_scanned_pdf(pdf_path):
    TEMP_FOLDER.mkdir(exist_ok=True)
    pdf = pdfium.PdfDocument(str(pdf_path))
    page_text = []

    try:
        for page_number in range(len(pdf)):
            page = pdf[page_number]
            bitmap = page.render(scale=2)
            pil_image = bitmap.to_pil()

            with tempfile.NamedTemporaryFile(
                suffix=".png",
                dir=TEMP_FOLDER,
                delete=False
            ) as temp_image:
                temp_path = Path(temp_image.name)

            try:
                pil_image.save(temp_path)
                extracted = _extract_text_from_image_file(temp_path).strip()
                if extracted:
                    page_text.append(extracted)
            finally:
                temp_path.unlink(missing_ok=True)
                pil_image.close()
    finally:
        pdf.close()

    return "\n\n".join(page_text)


def extract_text_from_pdf(pdf_path):
    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

    if extracted_text.strip():
        return extracted_text

    return _extract_text_from_scanned_pdf(pdf_path)


def extract_text_from_image(image_path):
    return _extract_text_from_image_file(image_path)
