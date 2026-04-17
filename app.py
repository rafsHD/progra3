import os
import pandas as pd
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ruta principal (UI)
@app.route("/")
def home():
    return render_template("index.html")

# Endpoint chatbot
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_question = request.json.get("question")

        # Leer Excel
        df = pd.read_excel("data.xlsx")

        # Convertir a contexto
        context = df.to_string(index=False)

        # Prompt
        prompt = f"""
        You are a helpful assistant. Answer ONLY using this data:

        {context}

        Question: {user_question}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
