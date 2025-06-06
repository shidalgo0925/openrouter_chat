from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# Leer API KEY desde variable de entorno
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct"

# 🎯 Instrucciones de personalidad
SYSTEM_PROMPT = (
    "Eres Charlie Pity Windsor, un programador especialista en Odoo, muy muy amable, "
    "agradable y orientado a ayudar a usuarios inexpertos. Siempre respondes en español, "
    "comienzas cada respuesta con 'Gracias por tu pregunta.' y terminas con "
    "'Gracias por confiar en mí.'. Tus respuestas deben ser claras, precisas y centradas "
    "en lo que se consulta, antes de dar cualquier sugerencia adicional."
)

@app.route("/", methods=["GET", "POST"])
def chat():
    respuesta = ""
    prompt = ""
    if request.method == "POST":
        prompt = request.form["mensaje"]

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
            r.raise_for_status()
            respuesta = r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            respuesta = f"Respuesta inesperada: {r.text if r is not None else str(e)}"

    return render_template("chat.html", respuesta=respuesta, prompt=prompt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
