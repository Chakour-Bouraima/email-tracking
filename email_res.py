from Database import insert_tracking_data

# Benutzer nach Name und E-Mail fragen
user_name = input("Bitte geben Sie den Benutzernamen ein: ")
email = input("Bitte geben Sie die E-Mail-Adresse ein: ")

# UUID generieren und speichern
unique_id = insert_tracking_data(user_name, email)

print(f"Tracking-URL für {user_name}: http://127.0.0.1:5000/pixel?id={unique_id}")
