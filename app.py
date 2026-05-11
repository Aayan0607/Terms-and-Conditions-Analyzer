from flask import Flask, render_template, request
from modules.extractor import extract_text_from_pdf, extract_text_from_image
from modules.analyzer import preprocess_text, segment_clauses
from modules.classifier import classify_clause
from modules.pipeline import analyze_contract
from modules.explanations import calculate_risk_score, generate_explanation
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

    # ANALYZE TEXT
    analysis_data = analyze_contract(extracted_text)

    return render_template(
        "results.html",
        results=analysis_data["results"],
        overall_risk=analysis_data["overall_risk"],
        severity_count=analysis_data["severity_count"],
        total_clauses=analysis_data["total_clauses"]
    )

if __name__ == '__main__':
    app.run(debug=True)