# Embedding model
MODEL_NAME = "all-MiniLM-L6-v2"

# Similarity thresholds
SIMILARITY_THRESHOLDS = {
    "critical": 0.72,
    "high": 0.62,
    "medium": 0.55,
    "low": 0.50
}

# Maximum allowed risk score
MAX_RISK_SCORE = 10

# OCR Path (Windows)
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Minimum words required for a valid clause
MIN_CLAUSE_WORDS = 5