from flask import Flask, render_template, request, send_file,Blueprint, redirect, url_for, flash, jsonify
from flask_mail import Mail, Message
import sqlite3
from PIL import Image
import io


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

def home():
    conn = sqlite3.connect('tracking.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, email, opened_at FROM email_tracking")
    daten = cursor.fetchall()
    conn.close()
    
    return render_template("index.html", daten=daten)
def track_email():
    uuid_received = request.args.get('id')

    img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    conn = sqlite3.connect('tracking.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, email FROM email_tracking WHERE uuid = ?", (uuid_received,))
    result = cursor.fetchone()

    if result:
        user_name, email = result
        print(f"E-Mail geöffnet von: {user_name} ({email})")

        # Update Öffnungszeit
        cursor.execute("UPDATE email_tracking SET opened_at = datetime('now', 'localtime') WHERE uuid = ?", (uuid_received,))
        conn.commit()
    conn.close()

    # Transparentes 1x1-Pixel-Bild zurückgeben
    return send_file(img_io, mimetype='image/png')

