# ---------------------------------------------------
# SEVERITY SCORING
# ---------------------------------------------------

SEVERITY_SCORES = {
    "low": 1,
    "medium": 3,
    "high": 5,
    "critical": 7
}


# ---------------------------------------------------
# UI COLORS
# ---------------------------------------------------

SEVERITY_COLORS = {
    "low": "green",
    "medium": "orange",
    "high": "orangered",
    "critical": "red"
}


# ---------------------------------------------------
# AGGRESSIVE LEGAL TERMS
# ---------------------------------------------------

AGGRESSIVE_TERMS = [

    # Company control
    "we reserve the right",
    "sole discretion",
    "without notice",
    "may change without notice",
    "terminate immediately",
    "access may be revoked",
    "may delete data",

    # Financial risks
    "non-refundable",
    "automatic renewal",
    "auto-debit authorization",

    # Privacy risks
    "share with advertisers",
    "sell your data",
    "track your location",
    "retain data indefinitely",

    # Legal protections for company
    "binding arbitration",
    "mandatory arbitration",
    "waive the right",
    "hold harmless",
    "release from liability",
    "exclusive jurisdiction",
    "class action waiver",
    "individual claims only",
    "disclaims all liability",

    # Ownership risks
    "worldwide license",
    "fully transferable",
    "content becomes our property",
    "irrevocable",
    "in perpetuity",

    # Extreme legal permanence
    "legally binding forever"
]