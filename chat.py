
from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "TU_API_KEY"

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
    app.run()
