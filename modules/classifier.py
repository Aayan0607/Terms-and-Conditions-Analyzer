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

    return {
        "category": best_category,
        "severity": best_severity,
        "similarity_score": round(float(best_similarity), 2),
        "description": best_description
    }