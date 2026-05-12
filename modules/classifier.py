import json
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from modules.config import (
    MODEL_NAME,
    SIMILARITY_THRESHOLDS
)

from modules.intent_rules import detect_intent


# LOAD MODEL
model = SentenceTransformer(MODEL_NAME)


# LOAD RISK DATASET
with open("datasets/risky_patterns.json", "r") as file:
    risky_patterns = json.load(file)


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


# ---------------------------------------------------
# MAIN CLASSIFIER
# ---------------------------------------------------

def classify_clause(clause):

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

        example_embeddings = model.encode(examples)

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
            "category": "Neutral",
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

        return {
            "category": "Neutral",
            "severity": "low",
            "similarity_score": round(float(final_score), 2),
            "description": (
                "This clause appears informational "
                "or operational."
            ),
            "intent": "neutral"
        }

    return {
        "category": best_category,
        "severity": best_severity,
        "similarity_score": round(float(final_score), 2),
        "description": best_description,
        "intent": "risky"
    }