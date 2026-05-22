# ---------------------------------------------------
# NEGATION TERMS
# ---------------------------------------------------

NEGATION_TERMS = [
    "not",
    "never",
    "no",
    "does not",
    "do not",
    "is not",
    "are not",
    "without",
    "will not",
    "won't"
]


# ---------------------------------------------------
# PROTECTIVE PHRASES
# ---------------------------------------------------

PROTECTIVE_PHRASES = [
    "users retain ownership",
    "retain full ownership",
    "with user consent",
    "advance notice",
    "user may cancel at any time",
    "user can unsubscribe",
    "user can opt out",
    "user has privacy controls",
    "optional feature",
    "not shared with advertisers",
    "does not collect",
    "never sold"
]


# ---------------------------------------------------
# RISK ACTION TERMS
# ---------------------------------------------------

RISK_ACTION_TERMS = [
    "share",
    "sell",
    "collect",
    "track",
    "transfer",
    "retain",
    "store",
    "disclose",
    "terminate",
    "suspend",
    "charge",
    "renew"
]


# ---------------------------------------------------
# INTENT DETECTION
# ---------------------------------------------------

def detect_intent(clause):
    clause_lower = clause.lower()

    has_negation = any(
        term in clause_lower
        for term in NEGATION_TERMS
    )

    has_risk_action = any(
        term in clause_lower
        for term in RISK_ACTION_TERMS
    )

    has_protective_phrase = any(
        phrase in clause_lower
        for phrase in PROTECTIVE_PHRASES
    )

    # Protective clause
    if (
        has_protective_phrase
    ):

        return "protective"

    if has_negation and has_risk_action:
        return "low-risk"

    if has_risk_action:
        return "risky"

    return "low-risk"
