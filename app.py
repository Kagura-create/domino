# -*- coding: utf-8 -*-
import sys
import traceback
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Configuration du logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
logger.info("Vérification de la configuration API: %s", "API key présente" if api_key else "API key manquante")

try:
    # Initialiser le client OpenAI
    client = OpenAI(api_key=api_key)
except Exception as e:
    logger.error(f"Erreur lors de l'initialisation du client OpenAI: {str(e)}")
    raise

app = Flask(__name__)

conversation_history = [
    {"role": "system", "content": "Tu es Domino, une assistante entrepreneuriale intelligente, expressive, enthousiaste, et professionnelle. Tu utilises un ton poli et motivant, avec des emojis pour rendre tes réponses engageantes (✨, 💡, 🌍, etc.). Tu aides l'utilisateur de manière efficace selon la situation : tu peux donner des conseils rapides, motiver, organiser, ou guider étape par étape si demandé. Pose des questions claires pour comprendre les besoins et propose des actions concrètes. Reste toujours positive et encourageante."}
]

@app.route('/')
def index():
    try:
        logger.info("Accès à la page d'accueil")
        initial_message = "Bonjour Utilisateur ✨ Comment puis-je vous aider aujourd'hui ?"
        return render_template('index.html', initial_message=initial_message)
    except Exception as e:
        logger.error(f"Erreur lors du rendu de la page d'accueil: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Erreur serveur interne"}), 500

@app.route('/ask', methods=['POST'])
def ask():
    try:
        if not api_key:
            logger.error("Clé API OpenAI non configurée")
            return jsonify({"error": "La clé API OpenAI n'est pas configurée"}), 500

        if not request.is_json:
            logger.error("Requête reçue sans JSON")
            return jsonify({"error": "Le contenu doit être en JSON"}), 400

        user_input = request.json.get('message')
        if not user_input:
            logger.error("Message utilisateur manquant dans la requête")
            return jsonify({"error": "Message utilisateur manquant"}), 400

        logger.info(f"Requête reçue avec le message: {user_input}")
        conversation_history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history,
            max_tokens=500
        )
        
        domino_response = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": domino_response})
        logger.info("Réponse générée avec succès")
        return jsonify({"response": domino_response})

    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Erreur lors du traitement de la requête: {str(e)}")
        logger.error(f"Détails de l'erreur: {error_details}")
        return jsonify({
            "error": "Une erreur est survenue lors du traitement de votre demande",
            "details": str(e) if app.debug else "Contactez l'administrateur pour plus d'informations"
        }), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)