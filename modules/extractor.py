import pdfplumber
import pytesseract
from PIL import Image
import os


# OPTIONAL
# Change path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(pdf_path):

    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:
            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

    return extracted_text


def extract_text_from_image(image_path):

    image = Image.open(image_path)

    # Convert to grayscale
    image = image.convert('L')

    # Increase contrast / threshold
    image = image.point(lambda x: 0 if x < 140 else 255)

    text = pytesseract.image_to_string(image)

    return text