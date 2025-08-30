from flask import Flask, request, render_template, jsonify, session
import requests
import re

app = Flask(__name__)
app.secret_key = "supersecretkey"

OPENROUTER_API_KEY = "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"
MODEL = "gpt-4.1-mini"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_doctor(prompt, conv_id):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    if "conversations" not in session:
        session["conversations"] = []

    while len(session["conversations"]) <= conv_id:
        session["conversations"].append([])

    messages = session["conversations"][conv_id]

    messages.append({
        "role": "user",
        "content": f"{prompt}\nRespond ONLY in medical context in this format:\nSymptoms:\nPossible Causes:\nRecommended Tests:\nAdvice:"
    })

    data = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 1000
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        res_json = response.json()
        answer = res_json["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": answer})
        session["conversations"][conv_id] = messages
        return answer
    else:
        return f"Error {response.status_code}: {response.text}"

@app.route("/")
def index():
    if "conversations" not in session:
        session["conversations"] = []
    return render_template("index.html", conversations=session["conversations"])

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    conv_id = data.get("conv_id", 0)
    user_input = data.get("message")
    answer = ask_doctor(user_input, conv_id)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
