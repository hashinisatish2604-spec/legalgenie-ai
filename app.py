import os
import uuid
import logging
from io import BytesIO

from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from gtts import gTTS

# =====================================================
# LOAD ENV VARIABLES
# =====================================================
load_dotenv()

# =====================================================
# IMPORT INTERNAL MODULES
# =====================================================

from views.chatbotLegalv2 import (
    process_input,
    create_new_chat,
    get_chat_list,
    load_chat
)

from views.judgmentPred import (
    extract_text_from_file,
    predict_verdict
)

from views.docGen import generate_document

# =====================================================
# FLASK APP INIT
# =====================================================

app = Flask(__name__)

# =====================================================
# LOGGING
# =====================================================

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)

# =====================================================
# DIRECTORIES
# =====================================================

AUDIO_DIR = os.path.join("static", "audio")
TEMP_DIR = "temp"

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# =====================================================
# ROUTES
# =====================================================

# ---------------- HOME / CHAT ----------------
@app.route("/")
def index():
    raw_chat_names = get_chat_list()
    chat_list = []

    for name in raw_chat_names:
        chat_data = load_chat(name)
        title = chat_data["past"][0][:30] + "..." if chat_data["past"] else "New Chat"
        chat_list.append({"name": name, "title": title})

    chat_name = chat_list[0]["name"] if chat_list else create_new_chat()

    return render_template(
        "index.html",
        chat_name=chat_name,
        chat_list=reversed(chat_list)
    )

# ---------------- NEW CHAT ----------------
@app.route("/new_chat", methods=["POST"])
def new_chat():
    name = create_new_chat()
    return jsonify({"chat_name": name})

# ---------------- CHAT API ----------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    user_input = data.get("user_input", "")
    chat_name = data.get("chat_name", "")
    language = data.get("language", "en")

    if not user_input or not chat_name:
        return jsonify({"error": "Missing input"}), 400

    response, source = process_input(
        chat_name=chat_name,
        user_input=user_input,
        language=language,
        return_source=True
    )

    audio_url = None
    try:
        lang_map = {"en": "en", "hi": "hi", "kn": "kn"}
        tts_lang = lang_map.get(language, "en")

        audio_file = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_file)

        gTTS(text=response, lang=tts_lang).save(audio_path)
        audio_url = f"/static/audio/{audio_file}"

    except Exception as e:
        app.logger.error(f"TTS Error: {e}")

    return jsonify({
        "response": response,
        "source": source,
        "audio_url": audio_url
    })

# =====================================================
# DOCUMENT PREDICTION
# =====================================================

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html")

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    language = request.form.get("language", "en")

    if "." not in file.filename:
        return jsonify({"error": "Invalid file"}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_{file.filename}")
    file.save(temp_path)

    try:
        extracted_text = extract_text_from_file(temp_path, ext)
        result = predict_verdict(extracted_text, language)
        return jsonify(result)

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# =====================================================
# DOCUMENT GENERATION ✅ FIXED
# =====================================================

@app.route("/generate", methods=["GET", "POST"])
def generate():
    if request.method == "GET":
        return render_template("generate.html")

    try:
        data = request.json
        doc_type = data.get("doc_type")
        form_data = data.get("form_data", {})

        if not doc_type or not form_data:
            return jsonify({"error": "Invalid input"}), 400

        # ✅ generate_document RETURNS A DOCX OBJECT
        doc = generate_document(doc_type, form_data)

        # ✅ SAVE USING BYTESIO (RENDER SAFE)
        file_stream = BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)

        return send_file(
            file_stream,
            as_attachment=True,
            download_name=f"{doc_type}.docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        app.logger.error("🔥 DOCUMENT GENERATION ERROR", exc_info=True)
        return jsonify({"error": str(e)}), 500

# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
