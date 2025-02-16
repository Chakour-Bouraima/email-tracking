from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("ENCRYPTION_KEY")
 # Zurück in Bytes konvertieren
print("🔑 Geladener Schlüssel:", key)
