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

Analyze the following legal document and provide:

1. Document Type
2. Legal Validity (Valid / Possibly Invalid)
3. Key Legal Issues
4. Missing Clauses (if any)
5. Suggestions for Improvement

Document:
{text}
"""

    analysis = call_llm(
        prompt,
        system_prompt="You are a legal judgment prediction assistant."
    )

    return {
        "document_type": "Predicted Legal Document",
        "analysis": analysis
    }
