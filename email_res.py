import sqlite3
import uuid

# Verbindung zur Datenbank
conn = sqlite3.connect('tracking.db')
cursor = conn.cursor()

# UUID generieren
unique_id = str(uuid.uuid4())
user_name = "Max Mustermann"
email = "max@example.com"

# UUID mit Benutzerdaten speichern
cursor.execute("INSERT INTO email_tracking (uuid, user_name, email) VALUES (?, ?, ?)", 
               (unique_id, user_name, email))

conn.commit()
conn.close()

print(f"Tracking-URL für {user_name}: https://127.0.0.1/pixel?id={unique_id}")