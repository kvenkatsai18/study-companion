"""
Study Companion — AI Learning Partner
Flask backend with voice I/O, MiniMax AI, and animated avatar
"""

import os
import re
import asyncio
from flask import Flask, render_template, request, jsonify, Response
import edge_tts
import httpx
import json

app = Flask(__name__)

# Config
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MINIMAX_GROUP_ID = os.environ.get("MINIMAX_GROUP_ID", "2040366535372976713")
MINIMAX_URL = "https://api.minimax.chat/v1/text/chatcompletion_v2"

VOICE = "en-US-AriaNeural"
SYSTEM_PROMPT = """You are a friendly, knowledgeable AI study companion. You help students learn, research, and practice. You speak in a warm, encouraging tone. You can explain concepts clearly, help with exam prep, create practice questions, and assist with research. Keep responses conversational but informative. If you don't know something, say so honestly."""


def get_history():
    history_file = os.path.join(os.path.dirname(__file__), "history.json")
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                return json.load(f)
        except:
            return []
    return []


def save_history(messages):
    history_file = os.path.join(os.path.dirname(__file__), "history.json")
    try:
        with open(history_file, "w") as f:
            json.dump(messages[-50:], f)
    except:
        pass


async def text_to_speech(text: str) -> bytes:
    communicate = edge_tts.Communicate(text, VOICE)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data


def get_ai_response(messages: list) -> str:
    print(f"[DEBUG] MINIMAX_API_KEY present: {bool(MINIMAX_API_KEY)}")
    print(f"[DEBUG] MINIMAX_API_KEY length: {len(MINIMAX_API_KEY) if MINIMAX_API_KEY else 0}")
    
    if not MINIMAX_API_KEY:
        return "Error: MiniMax API key is not configured on the server."

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "MiniMax-Text-01",
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.7
    }

    print(f"[DEBUG] Sending request to MiniMax API...")
    try:
        response = httpx.post(MINIMAX_URL, headers=headers, json=payload, timeout=60.0)
        print(f"[DEBUG] Response status: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        print(f"[DEBUG] Response data: {str(data)[:500]}")
        choices = data.get("choices", [])
        if choices:
            return choices[0]["message"]["content"]
        return "Sorry, I couldn't generate a response."
    except httpx.TimeoutException:
        print("[DEBUG] Request timed out")
        return "Request timed out. Please try again."
    except httpx.HTTPStatusError as e:
        print(f"[DEBUG] HTTP error: {e.response.status_code} - {e.response.text[:500]}")
        return f"API error {e.response.status_code}: {e.response.text[:200]}"
    except Exception as e:
        print(f"[DEBUG] Exception: {str(e)}")
        return f"Error: {str(e)}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    print(f"[DEBUG] /api/chat called. ENV KEY: {bool(os.environ.get('MINIMAX_API_KEY'))}")
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + get_history()
    messages.append({"role": "user", "content": user_message})
    response_text = get_ai_response(messages)
    messages.append({"role": "assistant", "content": response_text})
    save_history(messages[1:])
    return jsonify({"response": response_text})


@app.route("/api/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Empty text"}), 400

    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = text[:2000]

    async def generate():
        audio = await text_to_speech(text)
        yield audio

    return Response(generate(), mimetype="audio/mpeg")


@app.route("/api/history", methods=["GET"])
def history():
    return jsonify({"messages": get_history()})


@app.route("/api/clear", methods=["POST"])
def clear_history():
    save_history([])
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    print("Study Companion starting...")
    print(f"MiniMax API: {'Configured' if MINIMAX_API_KEY else 'NOT CONFIGURED'}")
    app.run(host="0.0.0.0", port=5000, debug=True)
