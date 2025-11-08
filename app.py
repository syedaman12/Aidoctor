import os
from flask import Flask, request, render_template, jsonify, session
import requests
from dotenv import load_dotenv 


from flask_cors import CORS  # Optional if you want to allow cross-origin requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")  # Use env var for security
CORS(app)

# Load API key from environment variable
OPENROUTER_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-4.1-mini"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_doctor(prompt, conv_id):
    """Send user input to OpenRouter API and return response"""
    
    # Initialize session conversations
    if "conversations" not in session:
        session["conversations"] = []

    while len(session["conversations"]) <= conv_id:
        session["conversations"].append([])

    messages = session["conversations"][conv_id]

    # Append user message with instruction for medical context
    messages.append({
        "role": "user",
        "content": f"{prompt}\nRespond ONLY in medical context in this format:\n"
                   f"Symptoms:\nPossible Causes:\nRecommended Tests:\nAdvice:"
    })

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 1000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()  # Raise error for bad status codes
        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            answer = data["choices"][0]["message"]["content"]
        else:
            answer = "No response from AI. Please try again."

        # Append AI response
        messages.append({"role": "assistant", "content": answer})
        session["conversations"][conv_id] = messages
        return answer

    except requests.exceptions.RequestException as e:
        return f"API Error: {str(e)}"

@app.route("/")
def index():
    if "conversations" not in session:
        session["conversations"] = []
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    conv_id = data.get("conv_id", 0)
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"answer": " Hello! I'm your AI Doctor."}), 400

    answer = ask_doctor(user_input, conv_id)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
