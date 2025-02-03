from flask import Flask
from routes import track_email  # Importiere die Routen aus routes.py

app = Flask(__name__)

# Registriere die Route aus routes.py
app.add_url_rule('/pixel', 'track_email', track_email)
app.add_url_rule('/', 'home', track_email)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
