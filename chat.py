
from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("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") or "TU_API_KEY"

MODEL = "mistralai/mistral-7b-instruct"

@app.route("/", methods=["GET", "POST"])
def chat():
    respuesta = ""
    prompt = ""
    if request.method == "POST":
        prompt = request.form["mensaje"]
        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
            respuesta = r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            respuesta = f"Error: {str(e)}"
    return render_template("chat.html", respuesta=respuesta, prompt=prompt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
