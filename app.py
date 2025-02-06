from flask import Flask
from email_send import send_email
from routes import home, track_email,send_email_bp   # Importiere die Routen aus routes.py

app = Flask(__name__)
# Blueprint registrieren
app.register_blueprint(send_email_bp)
# Registriere die Route aus routes.py
app.add_url_rule('/', 'home', home)
app.add_url_rule('/pixel', 'track_email', track_email)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
