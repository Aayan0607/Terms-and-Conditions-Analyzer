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

    # -----------------------------------
    # PREPROCESSING
    # -----------------------------------

    cleaned_text = preprocess_text(text)

    clauses = segment_clauses(cleaned_text)

    # -----------------------------------
    # STORAGE
    # -----------------------------------

    results = []

    severity_count = {
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0
    }

    # -----------------------------------
    # CLAUSE ANALYSIS
    # -----------------------------------

    for i, clause in enumerate(clauses, 1):

        # Ignore meaningless fragments
        if len(clause.split()) < 6:
            continue

        # Classification
        result = classify_clause(clause)

        # Risk score
        risk_score = calculate_risk_score(
            result["similarity_score"],
            result["severity"],
            clause
        )

        # Explanation
        explanation = generate_explanation(
            result["category"],
            result["description"],
            clause
        )

        # Count only actual risky clauses
        if result["intent"] == "risky":

            severity_count[result["severity"]] += 1

        # Store result
        results.append({
            "clause_number": i,
            "text": clause,
            "category": result["category"],
            "severity": result["severity"],
            "similarity": result["similarity_score"],
            "risk_score": risk_score,
            "intent": result["intent"],
            "explanation": explanation
        })

    # -----------------------------------
    # SORT RESULTS
    # -----------------------------------

    results.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    # -----------------------------------
    # OVERALL RISK CALCULATION
    # -----------------------------------

    risky_results = [
        r for r in results
        if r["intent"] == "risky"
    ]

    # Prevent division by zero
    if len(risky_results) == 0:

        average_risk = 0

    else:

        average_risk = round(
            sum(r["risk_score"] for r in risky_results)
            / len(risky_results),
            1
        )

    # Final contract risk level
    if average_risk >= 8:

        overall_risk = "CRITICAL"

    elif average_risk >= 6:

        overall_risk = "HIGH"

    elif average_risk >= 4:

        overall_risk = "MEDIUM"

    else:

        overall_risk = "LOW"

    # -----------------------------------
    # FINAL OUTPUT
    # -----------------------------------

    return {
        "results": results,
        "severity_count": severity_count,
        "overall_risk": overall_risk,
        "total_clauses": len(results)
    }