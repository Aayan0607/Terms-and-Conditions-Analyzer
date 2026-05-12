from modules.analyzer import (
    preprocess_text,
    segment_clauses
)

from modules.classifier import classify_clause

from modules.explanations import (
    calculate_risk_score,
    generate_explanation
)


def analyze_contract(text):

    cleaned_text = preprocess_text(text)

    clauses = segment_clauses(cleaned_text)

    results = []

    severity_count = {
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0
    }

    # Analyze clauses
    for i, clause in enumerate(clauses, 1):

        # Ignore tiny or meaningless fragments
        if len(clause.split()) < 6:
            continue

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

    # Sort highest risk first
    results.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    # Overall risk
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

    return {
        "results": results,
        "severity_count": severity_count,
        "overall_risk": overall_risk,
        "total_clauses": len(results)
    }