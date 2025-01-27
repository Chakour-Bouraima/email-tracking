import sqlite3
import uuid

# Verbindung zur Datenbank
conn = sqlite3.connect('tracking.db')
cursor = conn.cursor()


# Benutzer nach Name und E-Mail fragen
user_name = input("Bitte geben Sie den Benutzernamen ein: ")
email = input("Bitte geben Sie die E-Mail-Adresse ein: ")

# UUID generieren
unique_id = str(uuid.uuid4())


# UUID mit Benutzerdaten speichern
cursor.execute("INSERT INTO email_tracking (uuid, user_name, email) VALUES (?, ?, ?)", 
               (unique_id, user_name, email))

conn.commit()
conn.close()

print(f"Tracking-URL für {user_name}: http://127.0.0.1:5000/pixel?id={unique_id}")