import spacy
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import numpy as np

# Load spaCy
nlp = spacy.load("en_core_web_sm")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


def preprocess_text(text):

    text = text.replace("\n", " ")

    return text.strip()


def segment_clauses(text):

    doc = nlp(text)

    # Extract sentences
    sentences = [sent.text.strip() for sent in doc.sents]

    if len(sentences) <= 1:
        return sentences

    # Generate embeddings
    embeddings = model.encode(sentences)

    # Dynamic cluster count
    n_clusters = max(2, len(sentences) // 3)

    clustering = AgglomerativeClustering(
        n_clusters=n_clusters
    )

    labels = clustering.fit_predict(embeddings)

    # Group sentences by cluster
    clustered_sentences = {}

    for idx, label in enumerate(labels):

        if label not in clustered_sentences:
            clustered_sentences[label] = []

        clustered_sentences[label].append(
            (idx, sentences[idx])
        )

    # Preserve original order
    ordered_clauses = []

    for label in clustered_sentences:

        sorted_group = sorted(clustered_sentences[label])

        clause = " ".join(
            sentence for _, sentence in sorted_group
        )

        ordered_clauses.append(
            (sorted_group[0][0], clause)
        )

    # Sort clauses back into original document order
    ordered_clauses.sort(key=lambda x: x[0])

    final_clauses = [clause for _, clause in ordered_clauses]

    return final_clauses