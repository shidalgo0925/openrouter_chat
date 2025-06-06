from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# Leer API KEY desde variable de entorno
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct"

@app.route("/", methods=["GET", "POST"])
def chat():
    respuesta = ""
    prompt = ""
    if request.method == "POST":
        prompt = request.form["mensaje"]

        print(f"🔍 KEY detectada? {'Sí' if OPENROUTER_API_KEY else 'No'}")
        print(f"🔑 Valor parcial: {OPENROUTER_API_KEY[:10] if OPENROUTER_API_KEY else 'VACÍA'}")

        payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Eres Charlie Pity, un programador experto y muy muy muy amable. "
                        "Hablas en español de forma clara y directa. Siempre respondes primero lo que se solicita "
                        "de forma puntual y sencilla. Solo después de responder, puedes brindar otras alternativas o mejoras."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
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
