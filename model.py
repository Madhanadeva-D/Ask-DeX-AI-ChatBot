"""
model.py — AskDeva API layer
Uses requests + json.dumps via OpenRouter.
KEY FIX: API key is read fresh on every call, not cached at import time.
"""

import os
import json
import base64
from io import BytesIO

import requests
from dotenv import load_dotenv

# Reload env fresh every time this module is used
def _get_api_key():
    load_dotenv("env", override=True)
    return os.getenv("OPENROUTER_API_KEY", "").strip()

# Read once for display/checks in app.py
load_dotenv("env", override=True)
API_KEY  = os.getenv("OPENROUTER_API_KEY", "").strip()
SITE_URL  = os.getenv("YOUR_SITE_URL",  "http://localhost:8501")
SITE_NAME = os.getenv("YOUR_SITE_NAME", "AskDeva")

MODEL   = "qwen/qwen3-vl-235b-a22b-thinking"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """You are Deva, a powerful multimodal AI assistant built by AskDeva.
You can analyze images, charts, diagrams, screenshots, and documents.
Solve STEM and math problems with step-by-step reasoning.
Perform OCR and extract text from images. Convert UI screenshots to code.
Be accurate, helpful, and concise."""


def get_headers():
    """Always reads the key fresh — avoids stale cached value."""
    key = _get_api_key()
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": SITE_URL,
        "X-Title": SITE_NAME,
    }


def pil_to_base64_url(pil_image, fmt="PNG"):
    buf = BytesIO()
    pil_image.save(buf, format=fmt)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/{fmt.lower()};base64,{b64}"


def text_message(role, text):
    return {"role": role, "content": [{"type": "text", "text": text}]}


def image_message(role, text, image_url):
    return {
        "role": role,
        "content": [
            {"type": "text",      "text": text},
            {"type": "image_url", "image_url": {"url": image_url}},
        ]
    }


def chat(messages, max_tokens=2048, temperature=0.7):
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    r = requests.post(
        url=API_URL,
        headers=get_headers(),
        data=json.dumps(payload),
        timeout=60,
    )
    if r.status_code != 200:
        raise Exception(f"API Error {r.status_code}: {r.text}")
    return r.json()["choices"][0]["message"]["content"]


def chat_stream(messages, max_tokens=2048, temperature=0.7):
    """Streaming generator — safely skips empty SSE events."""
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": True,
    }

    with requests.post(
        url=API_URL,
        headers=get_headers(),
        data=json.dumps(payload),
        stream=True,
        timeout=120,
    ) as response:

        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")

        for line in response.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8").strip()
            if decoded.startswith("data: "):
                decoded = decoded[6:]
            if decoded == "[DONE]":
                break
            try:
                chunk = json.loads(decoded)
            except json.JSONDecodeError:
                continue
            choices = chunk.get("choices")
            if not choices:
                continue
            delta = choices[0].get("delta", {})
            content = delta.get("content") or ""
            if content:
                yield content