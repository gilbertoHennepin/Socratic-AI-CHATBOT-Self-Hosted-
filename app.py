from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Ollama server settings
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"

SYSTEM_PROMPT = (
    "You are a Socratic tutor. Ask guiding questions first; "
    "then hints; only full answers if explicitly requested."
)

def chat_ollama(messages):
    """Send conversation to Ollama and return model response."""
    payload = {"model": MODEL, "messages": messages, "stream": False}
    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["message"]["content"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Build messages list (system + user)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    # Ask Ollama
    bot_reply = chat_ollama(messages)

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
