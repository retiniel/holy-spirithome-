from flask import Flask, render_template, send_from_directory, jsonify, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Charger les variables d'environnement (.env)
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="static")

# === Configuration email ===
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# === Routes principales ===

@app.route('/')
def home():
    # renvoie le fichier index.html
    return send_from_directory('static', 'index.html')

@app.route('/send_prayer', methods=['POST'])
def send_prayer():
    try:
        data = request.get_json()
        name = data.get('name', 'Anonyme')
        email = data.get('email', 'Non renseigné')
        subject_text = data.get('subjectText', '(vide)')

        # Construire le message email
        msg = Message(
            subject=f"Sujet de prière — {name}",
            recipients=[os.getenv('RECEIVER_EMAIL')],
            body=f"""
        Nouveau sujet de prière reçu sur Holy Spirit Home 🙏

        Nom : {name}
        Email : {email}

        Sujet :
        {subject_text}

        — Message automatique du site Holy Spirit Home —
        """
        )

        mail.send(msg)
        print("✅ Email envoyé avec succès à", os.getenv('RECEIVER_EMAIL'))
        return jsonify({"success": True})

    except Exception as e:
        print("❌ Erreur :", e)
        return jsonify({"success": False, "error": str(e)}), 500


# === Lancer localement ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
