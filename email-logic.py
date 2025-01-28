from flask import Flask, request, send_file
import sqlite3
from PIL import Image
import io



app = Flask(__name__)

@app.route('/pixel')
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
        cursor.execute("UPDATE email_tracking SET opened_at = datetime('now') WHERE uuid = ?", (uuid_received,))
        conn.commit()
    conn.close()

    # Transparentes 1x1-Pixel-Bild zurückgeben
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(port=5000,debug=True)
