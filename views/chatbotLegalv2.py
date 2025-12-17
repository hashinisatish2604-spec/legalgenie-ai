import json
import os
import sys
from dotenv import load_dotenv

from utils.groq_client import call_llm

load_dotenv()

# ---------------- Redis Init ----------------
# NOTE: Minimal change: remove localhost Redis fallback (Render has no local Redis)

redis_client = None

UPSTASH_REDIS_URL = os.getenv("UPSTASH_REDIS_URL")
UPSTASH_REDIS_TOKEN = os.getenv("UPSTASH_REDIS_TOKEN")

if UPSTASH_REDIS_URL and UPSTASH_REDIS_TOKEN:
    try:
        from upstash_redis import Redis
        redis_client = Redis(
            url=UPSTASH_REDIS_URL,
            token=UPSTASH_REDIS_TOKEN
        )
        print("✅ Upstash Redis connected.", file=sys.stderr)
    except Exception as e:
        print("⚠️ Upstash Redis init failed:", e, file=sys.stderr)
        redis_client = None
else:
    print("⚠️ Redis disabled (no Upstash env vars).", file=sys.stderr)

# ---------------- System Prompt ----------------
SYSTEM_PROMPT = """
You are an AI Legal Assistant specialized in Indian law.
Provide accurate, clear, concise, educational answers.
This is not legal advice.
"""

LANGUAGE_MAP = {
    "en": "Respond in English.",
    "hi": "Respond in Hindi using Devanagari script.",
    "kn": "Respond in Kannada script."
}

# ---------------- Redis Helpers ----------------
def load_chat(chat_name: str) -> dict:
    if not redis_client:
        return {"past": [], "generated": []}

    data = redis_client.get(chat_name)
    if data:
        return json.loads(data)
    return {"past": [], "generated": []}

def save_chat(chat_name: str, chat_data: dict):
    if not redis_client:
        return
    redis_client.set(chat_name, json.dumps(chat_data))

def create_new_chat() -> str:
    if not redis_client:
        return "Chat 1"

    name = f"Chat {len(redis_client.keys('*')) + 1}"
    save_chat(name, {"past": [], "generated": []})
    return name

def get_chat_list() -> list:
    # Minimal safety fix: avoid crash when Redis is disabled
    if not redis_client:
        return []
    try:
        return list(redis_client.keys("*"))
    except Exception as e:
        print("Redis error:", e, file=sys.stderr)
        return []

# ---------------- Main Chat Logic ----------------
def process_input(chat_name: str, user_input: str, language="en", return_source=False):
    try:
        chat = load_chat(chat_name)

        history_text = ""
        for q, a in list(zip(chat["past"], chat["generated"]))[-5:]:
            history_text += f"User: {q}\nAssistant: {a}\n"

        language_instruction = LANGUAGE_MAP.get(language, "Respond in English.")

        prompt = f"""
{SYSTEM_PROMPT}

{language_instruction}

Conversation history:
{history_text}

User question:
{user_input}
"""

        response = call_llm(prompt)

        chat["past"].append(user_input)
        chat["generated"].append(response)
        save_chat(chat_name, chat)

        if return_source:
            return response, "GROQ"
        return response

    except Exception as e:
        error = f"Error: {str(e)}"
        if return_source:
            return error, "ERR"
        return error
