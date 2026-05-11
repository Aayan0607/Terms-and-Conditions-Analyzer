from modules.utils import SEVERITY_SCORES, AGGRESSIVE_TERMS

def calculate_risk_score(similarity, severity, clause):

    # Base score from severity
    base_score = SEVERITY_SCORES.get(severity, 5)

    # Similarity boost
    similarity_boost = similarity * 2

    # Aggressive phrase boost
    aggressive_boost = 0

    clause_lower = clause.lower()

    for term in AGGRESSIVE_TERMS:

        if term in clause_lower:
            aggressive_boost += 0.5

    final_score = base_score + similarity_boost + aggressive_boost

    # Cap at 10
    final_score = min(final_score, 10)

    return round(final_score, 1)


def generate_explanation(category, description, clause):

    explanation = f"""
    This clause was classified under '{category}'.

    Reason:
    {description}

    The system detected language patterns that may reduce user control,
    increase company authority, or affect privacy/security rights.
    """

    return explanation.strip()