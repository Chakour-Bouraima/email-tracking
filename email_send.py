from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Mail, Message

import os

send_email_bp = Blueprint('send_email_bp', __name__)

# Konfiguriere den Gmail-SMTP-Server
mail = Mail()

def configure_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Ändere zu deiner Gmail-Adresse
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Nutze ein App-Passwort
    mail.init_app(app)

@send_email_bp.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        recipient = request.form['recipient']
        subject = request.form['subject']
        message_body = request.form['message']
        
        msg = Message(subject, sender=os.environ.get('MAIL_USERNAME'), recipients=[recipient])
        msg.body = message_body
        
        try:
            mail.send(msg)
            flash('E-Mail erfolgreich gesendet!', 'success')
        except Exception as e:
            flash(f'Fehler beim Senden: {e}', 'danger')
        
        return redirect(url_for('send_email_bp.send_email'))
    
    return render_template('send_email.html')

@send_email_bp.route('/send_email_api', methods=['POST'])
def send_email_api():
    data = request.get_json()
    recipient = data.get('recipient')
    subject = data.get('subject')
    message_body = data.get('message')
    
    if not recipient or not subject or not message_body:
        return jsonify({"error": "Missing required fields"}), 400
    
    msg = Message(subject, sender=os.environ.get('MAIL_USERNAME'), recipients=[recipient])
    msg.body = message_body
    
    try:
        mail.send(msg)
        return jsonify({"message": "E-Mail erfolgreich gesendet!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
