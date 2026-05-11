from flask import Flask, render_template, request
from modules.extractor import extract_text_from_pdf, extract_text_from_image
from modules.analyzer import preprocess_text, segment_clauses
from modules.classifier import classify_clause
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

    cleaned_text = preprocess_text(extracted_text)

    clauses = segment_clauses(cleaned_text)

    for i, clause in enumerate(clauses, 1):
        print(f"\nCLAUSE {i}:")
        print(clause)

    results = []

    severity_count = {
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0
    }

    # Analyze all clauses
    for i, clause in enumerate(clauses, 1):

        result = classify_clause(clause)

        risk_score = calculate_risk_score(
            result["similarity_score"],
            result["severity"],
            clause
        )

        explanation = generate_explanation(
            result["category"],
            result["description"],
            clause
        )

        severity_count[result["severity"]] += 1

        results.append({
            "clause_number": i,
            "text": clause,
            "category": result["category"],
            "severity": result["severity"],
            "similarity": result["similarity_score"],
            "risk_score": risk_score,
            "explanation": explanation
        })

    # Sort by highest risk
    results.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    # Overall contract risk
    average_risk = round(
        sum(r["risk_score"] for r in results) / len(results),
        1
    )

    if average_risk >= 8:
        overall_risk = "CRITICAL"

    elif average_risk >= 6:
        overall_risk = "HIGH"

    elif average_risk >= 4:
        overall_risk = "MEDIUM"

    else:
        overall_risk = "LOW"

    formatted_output = f"""
    <h1>Contract Risk Summary</h1>

    <p><strong>Total Clauses:</strong> {len(results)}</p>

    <p><strong>Critical Risks:</strong> {severity_count['critical']}</p>

    <p><strong>High Risks:</strong> {severity_count['high']}</p>

    <p><strong>Medium Risks:</strong> {severity_count['medium']}</p>

    <p><strong>Low Risks:</strong> {severity_count['low']}</p>

    <h2>Overall Contract Risk: {overall_risk}</h2>

    <hr>
    """

    # Display sorted clauses
    for result in results:

        formatted_output += f"""
        <div style="border:1px solid black;
                    padding:15px;
                    margin:15px;">

            <h2>Clause {result['clause_number']}</h2>

            <p><strong>Text:</strong> {result['text']}</p>

            <p><strong>Category:</strong> {result['category']}</p>

            <p><strong>Severity:</strong> {result['severity']}</p>

            <p><strong>Similarity:</strong> {result['similarity']}</p>

            <p><strong>Risk Score:</strong> {result['risk_score']}/10</p>

            <p><strong>Explanation:</strong><br>
            {result['explanation']}</p>

        </div>
        """

    return formatted_output

if __name__ == '__main__':
    app.run(debug=True)