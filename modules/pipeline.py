from modules.analyzer import (
    preprocess_text,
    segment_clauses
)

from modules.classifier import classify_clause

from modules.explanations import (
    calculate_risk_score,
    generate_explanation
)
from modules.config import MIN_CLAUSE_WORDS


def _should_count_as_risky(severity, intent):
    return severity in {"medium", "high", "critical"} and intent != "protective"


def _is_high_impact(severity, intent):
    return severity in {"high", "critical"} and intent != "protective"


def analyze_contract(text):

    # -----------------------------------
    # PREPROCESSING
    # -----------------------------------

    cleaned_text = preprocess_text(text)

    clauses = segment_clauses(cleaned_text)

    if not cleaned_text:
        return {
            "results": [],
            "severity_count": {
                "low": 0,
                "medium": 0,
                "high": 0,
                "critical": 0
            },
            "overall_risk": "LOW",
            "total_clauses": 0
        }

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
        if len(clause.split()) < MIN_CLAUSE_WORDS:
            continue

        # Classification
        result = classify_clause(clause)

        # Risk score
        risk_score = calculate_risk_score(
            result["similarity_score"],
            result["severity"],
            clause
        )

        if result["intent"] == "low-risk" and risk_score >= 4:
            result["severity"] = "medium"
            result["category"] = "Medium Risk Clause"
            result["intent"] = "medium-risk"

        # Explanation
        explanation = generate_explanation(
            result["category"],
            result["description"],
            clause
        )

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
        if _should_count_as_risky(r["severity"], r["intent"])
    ]

    risky_clause_count = len(risky_results)
    total_clause_count = len(results)
    risky_clause_ratio = (
        risky_clause_count / total_clause_count
        if total_clause_count
        else 0
    )
    high_impact_clause_count = sum(
        1 for r in results
        if _is_high_impact(r["severity"], r["intent"])
    )
    critical_clause_count = sum(
        1 for r in results
        if r["severity"] == "critical" and r["intent"] != "protective"
    )
    high_impact_clause_ratio = (
        high_impact_clause_count / total_clause_count
        if total_clause_count
        else 0
    )
    critical_clause_ratio = (
        critical_clause_count / total_clause_count
        if total_clause_count
        else 0
    )

    # Prevent division by zero
    if len(risky_results) == 0:

        average_risk = 0

    else:

        average_risk = round(
            sum(r["risk_score"] for r in risky_results)
            / len(risky_results),
            1
        )

    # Final contract risk level:
    # - CRITICAL/HIGH depend on the share of high-impact clauses.
    # - MEDIUM depends on the share of medium-or-above clauses.
    if critical_clause_ratio > 0.15:
        overall_risk = "CRITICAL"
    elif high_impact_clause_ratio > 0.15:
        overall_risk = "HIGH"
    elif risky_clause_ratio >= 0.05:
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
        "total_clauses": total_clause_count,
        "risky_clause_count": risky_clause_count,
        "risky_clause_ratio": round(risky_clause_ratio, 3),
        "high_impact_clause_count": high_impact_clause_count,
        "high_impact_clause_ratio": round(high_impact_clause_ratio, 3),
        "average_risk_score": average_risk
    }
