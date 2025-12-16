import json
import os
import re
import sys
from dotenv import load_dotenv
from upstash_redis import Redis

from utils.groq_client import call_llm

load_dotenv()

# ---------------- Redis Init ----------------
upstash_url = os.getenv("UPSTASH_REDIS_URL")
upstash_token = os.getenv("UPSTASH_REDIS_TOKEN")

if upstash_url and upstash_token:
    redis_client = Redis(url=upstash_url, token=upstash_token)
    print("✅ Upstash Redis connected.", file=sys.stderr)
else:
    import redis
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=0,
        decode_responses=True
    )
    print("✅ Local Redis connected.", file=sys.stderr)

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
    data = redis_client.get(chat_name)
    if data:
        return json.loads(data)
    return {"past": [], "generated": []}

def save_chat(chat_name: str, chat_data: dict):
    redis_client.set(chat_name, json.dumps(chat_data))

def create_new_chat() -> str:
    name = f"Chat {len(redis_client.keys('*')) + 1}"
    save_chat(name, {"past": [], "generated": []})
    return name

def get_chat_list() -> list:
    return list(redis_client.keys('*'))

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
