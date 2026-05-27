import tempfile
from pathlib import Path

from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

from modules.config import ALLOWED_UPLOAD_EXTENSIONS, MAX_UPLOAD_SIZE_MB, TEMP_FOLDER
from modules.extractor import extract_text_from_pdf, extract_text_from_image
from modules.pipeline import analyze_contract


frontend_bp = Blueprint(
    "frontend",
    __name__,
    template_folder="templates",
    static_folder="static"
)

TEMP_FOLDER.mkdir(exist_ok=True)


def _allowed_file(filename):
    return Path(filename).suffix.lower() in ALLOWED_UPLOAD_EXTENSIONS


def _render_home(error=None):
    return render_template("index.html", error=error, max_upload_size_mb=MAX_UPLOAD_SIZE_MB)


@frontend_bp.route("/")
def home():
    return _render_home()


@frontend_bp.route("/analyze", methods=["POST"])
def analyze():
    contract_text = (request.form.get("contract_text") or "").strip()
    uploaded_file = request.files.get("file")
    extracted_text = ""

    if not contract_text and not (uploaded_file and uploaded_file.filename):
        return _render_home("Add contract text or upload a PDF/image before running the analysis.")

    if contract_text:
        extracted_text = contract_text
    else:
        original_name = secure_filename(uploaded_file.filename)

        if not _allowed_file(original_name):
            return _render_home(
                "Unsupported file type. Upload a PDF, PNG, JPG, JPEG, WEBP, BMP, or TIFF image."
            )

        suffix = Path(original_name).suffix.lower()

        with tempfile.NamedTemporaryFile(
            suffix=suffix,
            dir=TEMP_FOLDER,
            delete=False
        ) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            uploaded_file.save(temp_path)

            if suffix == ".pdf":
                extracted_text = extract_text_from_pdf(temp_path)
            else:
                extracted_text = extract_text_from_image(temp_path)
        except Exception as exc:
            return _render_home(f"Could not read the uploaded file. {exc}")
        finally:
            temp_path.unlink(missing_ok=True)

    if not extracted_text.strip():
        return _render_home(
            "No readable text was found. Try a clearer image/PDF or paste the contract text directly."
        )

    try:
        analysis_data = analyze_contract(extracted_text)
    except Exception as exc:
        return _render_home(f"Analysis failed while processing the document. {exc}")

    if not analysis_data["results"]:
        return _render_home(
            "The document was read, but it did not contain enough readable clauses to analyze reliably."
        )

    # ── Accuracy / confidence metrics ─────────────────────────
    all_results = analysis_data["results"]

    # Overall average similarity (classification confidence)
    all_sims = [r["similarity"] for r in all_results if r["similarity"] is not None]
    overall_accuracy = round(
        (sum(all_sims) / len(all_sims) * 100) if all_sims else 0, 1
    )

    # Per-severity average similarity
    sev_sims = {"critical": [], "high": [], "medium": [], "low": []}
    for r in all_results:
        sev = r["severity"]
        if sev in sev_sims and r["similarity"] is not None:
            sev_sims[sev].append(r["similarity"])

    accuracy_by_severity = {
        sev: round((sum(vals) / len(vals) * 100) if vals else 0, 1)
        for sev, vals in sev_sims.items()
    }

    # Confidence band distribution (for pie chart)
    high_conf   = sum(1 for s in all_sims if s >= 0.70)
    medium_conf = sum(1 for s in all_sims if 0.40 <= s < 0.70)
    low_conf    = sum(1 for s in all_sims if s < 0.40)

    confidence_bands = {
        "High (≥70%)":    high_conf,
        "Medium (40-69%)": medium_conf,
        "Low (<40%)":      low_conf
    }

    return render_template(
        "results.html",
        results=all_results,
        overall_risk=analysis_data["overall_risk"],
        severity_count=analysis_data["severity_count"],
        total_clauses=analysis_data["total_clauses"],
        risky_clause_count=analysis_data["risky_clause_count"],
        high_impact_clause_count=analysis_data.get("high_impact_clause_count", 0),
        average_risk_score=analysis_data.get("average_risk_score", 0),
        risky_clause_ratio=analysis_data.get("risky_clause_ratio", 0),
        overall_accuracy=overall_accuracy,
        accuracy_by_severity=accuracy_by_severity,
        confidence_bands=confidence_bands
    )
