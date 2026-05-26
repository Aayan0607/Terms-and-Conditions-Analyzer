import json
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

from modules.config import (
    RISKY_PATTERNS_PATH,
    SIMILARITY_THRESHOLDS
)
from modules.model_store import get_embedding_model

from modules.intent_rules import detect_intent


# LOAD MODEL
model = get_embedding_model()


# LOAD RISK DATASET
with open(RISKY_PATTERNS_PATH, "r", encoding="utf-8") as file:
    risky_patterns = json.load(file)


RISK_REFERENCE_EMBEDDINGS = {
    category: model.encode(data["examples"])
    for category, data in risky_patterns.items()
}


# ---------------------------------------------------
# RISK SIGNAL WORDS
# ---------------------------------------------------

RISK_KEYWORDS = {
    "high": [
        "terminate",
        "liability",
        "indemnify",
        "waive",
        "sole discretion",
        "without notice",
        "binding arbitration",
    ],

    "medium": [
        "share data",
        "modify",
        "suspend",
        "restrict",
        "automatic renewal",
        "third party",
    ],

    "low": [
        "may",
        "retain",
        "collect",
        "store",
    ]
}


# ---------------------------------------------------
# KEYWORD BOOST
# ---------------------------------------------------

def keyword_risk_boost(clause):

    clause_lower = clause.lower()

    score = 0

    for severity, keywords in RISK_KEYWORDS.items():

        for keyword in keywords:

            if keyword in clause_lower:

                if severity == "high":
                    score += 0.20

                elif severity == "medium":
                    score += 0.10

                else:
                    score += 0.05

    return min(score, 0.35)


def build_fallback_description(best_category, best_description, fallback_severity):
    if not best_category or not best_description:
        return (
            "This clause does not strongly match the highest-risk patterns, "
            "but it still contains language worth reviewing."
        )

    severity_label = "medium" if fallback_severity == "medium" else "low"

    return (
        f"This clause is classified as {severity_label} risk because it only "
        f"partially matches the '{best_category}' category. Closest-match reason: "
        f"{best_description}"
    )


# ---------------------------------------------------
# MAIN CLASSIFIER
# ---------------------------------------------------

def classify_clause(clause):
    if not clause or len(clause.split()) < 3:
        return {
            "category": "Low Risk Clause",
            "severity": "low",
            "similarity_score": 0.0,
            "description": "This clause is too short to classify reliably.",
            "intent": "low-risk"
        }

    clause_embedding = model.encode([clause])

    best_category = None
    best_similarity = 0
    best_severity = None
    best_description = None

    # ---------------------------------------------------
    # SEMANTIC MATCHING
    # ---------------------------------------------------

    for category, data in risky_patterns.items():

        examples = data["examples"]

        example_embeddings = RISK_REFERENCE_EMBEDDINGS[category]

        similarities = cosine_similarity(
            clause_embedding,
            example_embeddings
        )[0]

        max_similarity = np.max(similarities)

        if max_similarity > best_similarity:

            best_similarity = max_similarity
            best_category = category
            best_severity = data["severity"]
            best_description = data["description"]

    # ---------------------------------------------------
    # INTENT ANALYSIS
    # ---------------------------------------------------

    intent = detect_intent(clause)

    # ---------------------------------------------------
    # KEYWORD BOOST
    # ---------------------------------------------------

    keyword_boost = keyword_risk_boost(clause)

    # ---------------------------------------------------
    # FINAL RISK SCORE
    # ---------------------------------------------------

    final_score = best_similarity + keyword_boost

    # Slight boost if intent appears risky
    if intent == "risky":
        final_score += 0.08

    final_score = min(final_score, 1.0)

    # ---------------------------------------------------
    # DYNAMIC THRESHOLD
    # ---------------------------------------------------

    required_threshold = SIMILARITY_THRESHOLDS.get(
        best_severity,
        0.45
    )

    # ---------------------------------------------------
    # PROTECTIVE CLAUSES
    # ---------------------------------------------------

    if intent == "protective":

        return {
            "category": "Protective Clause",
            "severity": "low",
            "similarity_score": round(float(final_score), 2),
            "description": (
                "This clause appears protective "
                "rather than harmful."
            ),
            "intent": "protective"
        }

    # ---------------------------------------------------
    # FINAL DECISION
    # ---------------------------------------------------

    if final_score < required_threshold:
        fallback_severity = "medium" if final_score >= 0.35 else "low"
        fallback_category = (
            "Medium Risk Clause"
            if fallback_severity == "medium"
            else "Low Risk Clause"
        )
        fallback_intent = (
            "medium-risk"
            if fallback_severity == "medium"
            else "low-risk"
        )

        return {
            "category": fallback_category,
            "severity": fallback_severity,
            "similarity_score": round(float(final_score), 2),
            "description": build_fallback_description(
                best_category,
                best_description,
                fallback_severity
            ),
            "intent": fallback_intent
        }

    return {
        "category": best_category,
        "severity": best_severity,
        "similarity_score": round(float(final_score), 2),
        "description": best_description,
        "intent": "risky"
    }
