from dotenv import load_dotenv
load_dotenv()

from PyPDF2 import PdfReader
from docx import Document
from utils.groq_client import call_llm

LANGUAGE_MAP = {
    "en": "Respond in English.",
    "hi": "Respond in Hindi using Devanagari script.",
    "kn": "Respond in Kannada script."
}

# ---------------- TEXT EXTRACTION ----------------
def extract_text_from_file(file_path, ext):
    text = ""

    if ext == "pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""

    elif ext in ["docx", "doc"]:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif ext == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    return text.strip()

# ---------------- PREDICTION ----------------
def predict_verdict(text, language="en"):
    prompt = f"""
You are an expert Indian legal analyst.

{LANGUAGE_MAP.get(language)}

Analyze the following legal document and provide the response in clearly labeled sections:

Document Type:
Legal Validity:
Key Legal Issues:
Missing Clauses:
Suggestions for Improvement:
Final Prediction (Favorable / Unfavorable / Uncertain):
Risk Level (Low / Medium / High):
Confidence Level (0–100%):

Document:
{text}
"""

    analysis = call_llm(
        prompt,
        system_prompt="You are a legal judgment prediction assistant."
    )

    # -------- SAFE PARSING (NO BREAKAGE) --------
    def extract_section(label):
        try:
            return analysis.split(label + ":")[1].split("\n")[0].strip()
        except Exception:
            return ""

    return {
        # EXISTING (DO NOT CHANGE)
        "document_type": extract_section("Document Type") or "Predicted Legal Document",
        "analysis": analysis,

        # NEW (OPTIONAL, SAFE)
        "prediction": extract_section("Final Prediction"),
        "risk_level": extract_section("Risk Level"),
        "confidence": extract_section("Confidence Level"),
        "issues": extract_section("Key Legal Issues"),
        "suggestions": extract_section("Suggestions for Improvement")
    }
