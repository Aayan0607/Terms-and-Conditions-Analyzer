import os
from pathlib import Path

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

# OCR Path (Windows default / overridable)
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_FOLDER = BASE_DIR / "temp"
MACOS_OCR_SCRIPT = BASE_DIR / "modules" / "macos_ocr.swift"
RISKY_PATTERNS_PATH = BASE_DIR / "datasets" / "risky_patterns.json"
ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}
MAX_UPLOAD_SIZE_MB = 20
DEFAULT_HOST = os.getenv("APP_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.getenv("APP_PORT", "5050"))
DEFAULT_DEBUG = os.getenv("APP_DEBUG", "").lower() in {"1", "true", "yes"}

# Minimum words required for a valid clause
MIN_CLAUSE_WORDS = 5
