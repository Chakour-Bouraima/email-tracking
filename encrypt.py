from Crypto.Cipher import AES
import base64
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env Datei
load_dotenv()
key = base64.urlsafe_b64decode(os.getenv("ENCRYPTION_KEY"))
def encrypt_aes_gcm(plaintext, key):
    nonce = os.urandom(12)  # Zufälliger 12-Byte Nonce
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    return base64.urlsafe_b64encode(nonce + tag + ciphertext).decode()  # Alle Daten zusammen speichern

def decrypt_aes_gcm(encrypted_data, key):
    encrypted_data = base64.urlsafe_b64decode(encrypted_data)
    nonce = encrypted_data[:12]  # Nonce wieder extrahieren
    tag = encrypted_data[12:28]  # Authentifizierungs-Tag extrahieren
    ciphertext = encrypted_data[28:]  # Verschlüsselten Text extrahieren

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)  # Entschlüsselerzeugung
    return cipher.decrypt_and_verify(ciphertext, tag).decode()  # Entschlüsseln

# Schlüssel generieren

text = encrypt_aes_gcm("hhshshshs", key)
print(text)
print(decrypt_aes_gcm(text,key))