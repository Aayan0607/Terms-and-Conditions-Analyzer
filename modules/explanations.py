from modules.utils import (
    SEVERITY_SCORES,
    AGGRESSIVE_TERMS
)


# ---------------------------------------------------
# RISK SCORE CALCULATION
# ---------------------------------------------------

def calculate_risk_score(similarity, severity, clause):

    clause_lower = clause.lower()

    # -----------------------------------
    # BASE SEVERITY SCORE
    # -----------------------------------

    base_score = SEVERITY_SCORES.get(
        severity,
        3
    )

    # -----------------------------------
    # SIMILARITY CONTRIBUTION
    # -----------------------------------

    similarity_boost = similarity * 2

    # -----------------------------------
    # AGGRESSIVE LEGAL LANGUAGE
    # -----------------------------------

    aggressive_boost = 0

    matched_terms = 0

    for term in AGGRESSIVE_TERMS:

        if term in clause_lower:

            matched_terms += 1

    # Controlled boosting
    aggressive_boost = min(
        matched_terms * 0.3,
        2
    )

    # -----------------------------------
    # FINAL SCORE
    # -----------------------------------

    final_score = (
        base_score
        + similarity_boost
        + aggressive_boost
    )

    # Keep within range
    final_score = max(1, min(final_score, 10))

    return round(final_score, 1)


# ---------------------------------------------------
# EXPLANATION GENERATION
# ---------------------------------------------------

def generate_explanation(category, description, clause):

    explanation = f"""
    This clause was classified under '{category}'.

    Reason:
    {description}

    The system detected legal or operational language patterns
    associated with potential user risk, reduced control,
    privacy concerns, financial obligations, or platform authority.
    """

    return explanation.strip()