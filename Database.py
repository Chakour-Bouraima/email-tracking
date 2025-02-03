import sqlite3
import uuid

def insert_tracking_data(user_name, email):
    conn = sqlite3.connect('tracking.db')
    cursor = conn.cursor()

    unique_id = str(uuid.uuid4())

    cursor.execute("INSERT INTO email_tracking (uuid, user_name, email) VALUES (?, ?, ?)", 
                   (unique_id, user_name, email))

    conn.commit()
    conn.close()

    return unique_id
