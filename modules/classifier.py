import json
import numpy as np

from sentence_transformers import SentenceTransformer
from modules.config import MODEL_NAME
from sklearn.metrics.pairwise import cosine_similarity

# Load embedding model
model = SentenceTransformer(MODEL_NAME)

# Load risky patterns
with open('datasets/risky_patterns.json', 'r') as file:
    risky_patterns = json.load(file)


def classify_clause(clause):

    clause_embedding = model.encode([clause])

    best_category = None
    best_similarity = 0
    best_severity = None
    best_description = None

    # Compare against all categories
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

    # Neutral threshold
    # Dynamic thresholds based on severity
    severity_thresholds = {
        "critical": 0.72,
        "high": 0.62,
        "medium": 0.55,
        "low": 0.50
    }

    required_threshold = severity_thresholds.get(best_severity, 0.60)

    # Neutral if similarity is too weak
    if best_similarity < required_threshold:

        return {
            "category": "Neutral",
            "severity": "low",
            "similarity_score": round(float(best_similarity), 2),
            "description": "This clause appears informational or operational rather than risky."
        }

    # NEGATION DETECTION
    NEGATION_TERMS = [
        "not",
        "never",
        "no",
        "does not",
        "do not",
        "is not",
        "are not",
        "without",
        "won't",
        "will not"
    ]

    POSITIVE_RISK_TERMS = [
        "share",
        "sell",
        "collect",
        "track",
        "transfer",
        "store",
        "retain",
        "disclose"
    ]

    SAFE_CONTEXT = [
        "with user consent",
        "users may cancel",
        "retain full ownership",
        "users retain ownership",
        "advance notice",
        "explicitly enables",
        "not shared with advertisers",
        "never sold",
        "does not collect",
        "not transferred",
        "may opt out",
        "can disable",
        "can unsubscribe",
        "subject to user approval",
        "privacy controls",
        "user controlled",
        "optional feature"
    ]

    clause_lower = clause.lower()

    has_negation = any(
        term in clause_lower for term in NEGATION_TERMS
    )

    has_risk_action = any(
        term in clause_lower for term in POSITIVE_RISK_TERMS
    )

    has_safe_context = any(
        phrase in clause_lower for phrase in SAFE_CONTEXT
    )

    # Reduce false positives for protective clauses
    if ((has_negation and has_risk_action)or has_safe_context):

        return {
            "category": "Neutral",
            "severity": "low",
            "similarity_score": round(float(best_similarity), 2),
            "description": "This clause appears to protect user rights rather than introduce harmful conditions."
        }

    return {
        "category": best_category,
        "severity": best_severity,
        "similarity_score": round(float(best_similarity), 2),
        "description": best_description
    }   