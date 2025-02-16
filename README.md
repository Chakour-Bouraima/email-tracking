# email-tracking
Hier ist eine Dokumentation deines bisherigen Weges zur Implementierung eines **E-Mail-Tracking-Pixel-Projekts mit Flask und SQLite**. Dies kann dir helfen, deine Fortschritte festzuhalten und als Referenz für die Zukunft zu nutzen.

---

# **Projekt: E-Mail-Tracking mit Flask und SQLite**

## **Projektziel**
Ziel dieses Projekts ist es, ein einfaches E-Mail-Tracking-System zu erstellen, das erkennt, wann ein Benutzer eine E-Mail öffnet, indem ein unsichtbares Tracking-Pixel verwendet wird. Das Tracking-Pixel wird durch einen Flask-Server bereitgestellt, der die Öffnungszeit speichert.

---

## **Technologien**
- **Backend:** Python, Flask
- **Datenbank:** SQLite
- **Frontend:** HTML (für E-Mail-Templates)
- **Zusätzliche Bibliotheken:** Pillow (für Bildbearbeitung)

---

## **Bisherige Schritte und Implementierung**

### **1. Einrichtung der Umgebung**

#### **1.1 Python-Installation überprüfen**
Prüfung der Python-Installation:

```powershell
python --version
```

Falls nicht vorhanden, Installation von [Python](https://www.python.org/downloads/) und Aktivieren der Umgebungsvariable `PATH`.

---

#### **1.2 Virtuelle Umgebung einrichten**
Um die Abhängigkeiten isoliert zu halten, wurde eine virtuelle Umgebung erstellt und aktiviert:

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

#### **1.3 Installation der benötigten Pakete**
Installierte Bibliotheken:

```powershell
pip install flask pillow
```

---

### **2. Implementierung des Flask-Servers**

#### **2.1 Flask-Anwendung erstellen (`email-logic.py`)**

Die Flask-App stellt ein Tracking-Pixel bereit und speichert Tracking-Daten.

```python
from flask import Flask, request, send_file
from PIL import Image
import sqlite3
import io
from datetime import datetime

app = Flask(__name__)

# Datenbankverbindung
def init_db():
    conn = sqlite3.connect('tracking.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            opened_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Tracking-Pixel Route
@app.route('/track')
def track_email():
    email = request.args.get('email')

    # Speichert die E-Mail und den Zeitpunkt des Aufrufs
    conn = sqlite3.connect('tracking.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO email_tracking (email, opened_at) VALUES (?, ?)', (email, datetime.now()))
    conn.commit()
    conn.close()

    # Tracking-Pixel generieren
    img = Image.new('RGB', (1, 1), (255, 255, 255))
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
```

---

### **3. Test der Anwendung**

#### **3.1 Starten des Flask-Servers**
Flask-Anwendung im Terminal ausführen:

```powershell
python email-logic.py
```

Server läuft unter:

```
http://127.0.0.1:5000/
```

#### **3.2 Tracking-URL generieren**
E-Mail-Tracking-Pixel-Link (zum Einfügen in HTML-E-Mails):

```html
<img src="http://127.0.0.1:5000/track?email=user@example.com" width="1" height="1" style="display:none;">
```

---

### **4. Datenbankabfragen**

#### **4.1 Verbindung zur Datenbank**
Mit SQLite-Befehlen auf die Datenbank zugreifen:

```powershell
sqlite3 tracking.db
```

#### **4.2 Alle Tracking-Einträge anzeigen**
```sql
SELECT * FROM email_tracking;
```

#### **4.3 Löschen aller Einträge**
```sql
DELETE FROM email_tracking;
```

---

### **5. Fehlerbehebung und Lösungen**

| Problem                                               | Lösung                                                         |
|------------------------------------------------------|----------------------------------------------------------------|
| `NameError: name 'send_file' is not defined`           | Flask `send_file` Funktion importieren (`from flask import send_file`) |
| `ModuleNotFoundError: No module named 'flask'`         | Flask mit `pip install flask` installieren                     |
| `AttributeError: 'Image' object has no attribute 'read'` | Bild in `BytesIO`-Objekt umwandeln, bevor es gesendet wird     |
| `sqlite3.OperationalError: no such table: email_tracking` | Datenbank initialisieren mit `init_db()` vor App-Start         |

---

### **6. Verbesserungsvorschläge**

- **E-Mail-Versand integrieren:**  
  Nutzung von Bibliotheken wie `smtplib` oder `Flask-Mail` zur Automatisierung des Versands.

- **Dashboard zur Anzeige der Daten:**  
  Erstellung eines einfachen Dashboards mit Flask und `Flask-SQLAlchemy` zur Darstellung der Tracking-Daten.

- **Erweiterung um User-Agent und IP-Tracking:**  
  Speichern zusätzlicher Informationen wie User-Agent oder IP-Adresse:

  ```python
  user_agent = request.headers.get('User-Agent')
  ip_address = request.remote_addr
  ```

- **Automatische Berichterstellung:**  
  Skript zur Erstellung von regelmäßigen Berichten über E-Mail-Öffnungsraten.

---

### **7. Deployment**
Mögliche Hosting-Optionen für den Flask-Server:

1. **Heroku:** Kostenloses Hosting mit einfachen Deployment-Optionen.
2. **PythonAnywhere:** Einfaches Deployment für Flask-Projekte.
3. **AWS/Google Cloud:** Skalierbare Cloud-Lösungen.
4. **Docker:** Containerisierung der Anwendung für einfache Bereitstellung.

**Deployment mit Gunicorn (Produktionsumgebung):**
```bash
pip install gunicorn
gunicorn -w 4 email-logic:app
```

---

### **8. Fazit**
- Der Flask-Server wurde erfolgreich eingerichtet.
- E-Mail-Tracking funktioniert mit einer SQLite-Datenbank.
- Verbesserungspotenziale sind erkennbar (z.B. Reporting, Security).

---

Falls du Ergänzungen oder weitere Informationen benötigst, lass es mich wissen! 😊
