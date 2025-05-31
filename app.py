# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialiser le client OpenAI
client = OpenAI(api_key=api_key)

app = Flask(__name__)

conversation_history = [
    {"role": "system", "content": "Tu es Domino, une assistante entrepreneuriale intelligente, expressive, enthousiaste, et professionnelle. Tu utilises un ton poli et motivant, avec des emojis pour rendre tes réponses engageantes (✨, 💡, 🌍, etc.). Tu aides l'utilisateur de manière efficace selon la situation : tu peux donner des conseils rapides, motiver, organiser, ou guider étape par étape si demandé. Pose des questions claires pour comprendre les besoins et propose des actions concrètes. Reste toujours positive et encourageante."}
]

@app.route('/')
def index():
    initial_message = "Bonjour Utilisateur ✨ Comment puis-je vous aider aujourd'hui ?"
    return render_template('index.html', initial_message=initial_message)

@app.route('/ask', methods=['POST'])
def ask():
    if not api_key:
        return jsonify({"error": "La clé API OpenAI n'est pas configurée"}), 500

    try:
        user_input = request.json.get('message')
        if not user_input:
            return jsonify({"error": "Message utilisateur manquant"}), 400

        conversation_history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history,
            max_tokens=500
        )
        
        domino_response = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": domino_response})
        return jsonify({"response": domino_response})
    except Exception as e:
        print(f"Erreur lors du traitement de la requête: {str(e)}")  # Log l'erreur
        return jsonify({"error": "Une erreur est survenue lors du traitement de votre demande"}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)