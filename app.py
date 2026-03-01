from flask import Flask, request, Response
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"

def load_knowledge():
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        return f.read()

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    knowledge = load_knowledge()

    system_prompt = f"""
You are the official SaraCell Help Assistant.
Answer ONLY using the information below.

Knowledge Base:
{knowledge}

User Question:
{user_message}
"""

    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": system_prompt,
        "stream": True
    }

    def generate():
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                yield data.get("response", "")

    return Response(generate(), content_type="text/plain")

if __name__ == "__main__":
    app.run(debug=True)