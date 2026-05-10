from flask import Flask, render_template, request
from modules.extractor import extract_text_from_pdf, extract_text_from_image
import os

app = Flask(__name__)

TEMP_FOLDER = "temp"

os.makedirs(TEMP_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    contract_text = request.form.get('contract_text')

    uploaded_file = request.files.get('file')

    extracted_text = ""

    # CASE 1 → User pasted text
    if contract_text.strip():
        extracted_text = contract_text

    # CASE 2 → User uploaded file
    elif uploaded_file:

        filepath = os.path.join(TEMP_FOLDER, uploaded_file.filename)

        uploaded_file.save(filepath)

        if uploaded_file.filename.endswith('.pdf'):

            extracted_text = extract_text_from_pdf(filepath)

        else:
            extracted_text = extract_text_from_image(filepath)

        # DELETE FILE AFTER EXTRACTION
        os.remove(filepath)

    print(extracted_text)

    return extracted_text


if __name__ == '__main__':
    app.run(debug=True)