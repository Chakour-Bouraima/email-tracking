import sqlite3
import uuid
from encrypt import decrypt_aes_gcm,encrypt_aes_gcm,keyr
from dotenv import load_dotenv


def insert_tracking_data(user_name, email):
    conn = sqlite3.connect('tracking.db')
    cursor = conn.cursor()
    user_name_crp = encrypt_aes_gcm(user_name, keyr())
    email_crp = encrypt_aes_gcm(email, keyr())
    unique_id = str(uuid.uuid4())

    cursor.execute("INSERT INTO email_tracking (uuid, user_name, email) VALUES (?, ?, ?)", 
                   (unique_id, user_name_crp, email_crp))

    conn.commit()
    conn.close()

    return unique_id
