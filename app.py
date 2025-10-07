from flask import Flask, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'defaultsecret')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/send_prayer', methods=['POST'])
def send_prayer():
    data = request.get_json()
    name = data.get('name', 'Anonyme')
    email = data.get('email', 'Non fourni')
    subject_text = data.get('subjectText', '(vide)')

    msg = Message(
        subject=f"Sujet de prière - {name}",
        recipients=[os.getenv('RECEIVER_EMAIL')],
        body=f"Nom : {name}\nEmail : {email}\n\nSujet :\n{subject_text}"
    )

    try:
        mail.send(msg)
        return jsonify({'success': True, 'message': 'Email envoyé avec succès'})
    except Exception as e:
        print('Erreur:', e)
        return jsonify({'success': False, 'message': 'Erreur lors de l’envoi'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
