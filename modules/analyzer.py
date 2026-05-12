import re
import spacy
from sentence_transformers import SentenceTransformer, util

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load semantic embedding model
# Good lightweight option for semantic similarity
model = SentenceTransformer("all-MiniLM-L6-v2")


def preprocess_text(text):
    """
    Clean raw legal/document text.
    """

    # Remove extra spaces/newlines
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def semantic_similarity(sent1, sent2):
    """
    Compute semantic similarity between two sentences.
    """

    emb1 = model.encode(sent1, convert_to_tensor=True)
    emb2 = model.encode(sent2, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2).item()

    return score


def segment_clauses(text, similarity_threshold=0.55):
    """
    Context-aware clause segmentation.

    Groups semantically related sentences together
    instead of relying only on keywords.
    """

    text = preprocess_text(text)

    doc = nlp(text)

    # Step 1: Extract valid sentences
    sentences = []

    for sent in doc.sents:

        cleaned = sent.text.strip()

        # Ignore tiny fragments
        if len(cleaned.split()) < 4:
            continue

        # Ignore numeric/symbol garbage
        if re.fullmatch(r"[\d\W]+", cleaned):
            continue

        sentences.append(cleaned)

    if not sentences:
        return []

    # Step 2: Build semantic clauses
    clauses = []
    current_clause = [sentences[0]]

    for i in range(1, len(sentences)):

        prev_sent = sentences[i - 1]
        curr_sent = sentences[i]

        similarity = semantic_similarity(prev_sent, curr_sent)

        # If semantically related -> same clause
        if similarity >= similarity_threshold:
            current_clause.append(curr_sent)

        else:
            # Start new clause
            clauses.append(" ".join(current_clause))
            current_clause = [curr_sent]

    # Add final clause
    if current_clause:
        clauses.append(" ".join(current_clause))

    return clauses