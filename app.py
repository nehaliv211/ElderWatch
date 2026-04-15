from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import schedule
import time
import threading

app = Flask(__name__)
CORS(app)

# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    return "ElderWatch Backend is Running ✅"

# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_db():
    conn = sqlite3.connect("elderwatch.db")
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------
# CHECK LAST CHECK-IN
# -------------------------
def check_last_checkin():
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT time FROM checkin ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()

        if row:
            last_time = datetime.strptime(row["time"], "%Y-%m-%d %H:%M:%S")
            now = datetime.now()

            difference = now - last_time

            if difference.total_seconds() > 86400:
                print("⚠ ALERT: No check-in in last 24 hours!")

        conn.close()
    except Exception as e:
        print("Error in scheduler:", e)

# -------------------------
# SCHEDULER
# -------------------------
def run_scheduler():
    schedule.every(1).hours.do(check_last_checkin)

    while True:
        schedule.run_pending()
        time.sleep(1)

# -------------------------
# DAILY CHECK-IN
# -------------------------
@app.route("/checkin", methods=["POST"])
def checkin():
    data = request.json
    status = data.get("status", "OK")
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    conn.execute(
        "INSERT INTO checkin (status,time) VALUES (?,?)",
        (status, time_now)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Check-in recorded"})

# -------------------------
# GET CHECK-INS
# -------------------------
@app.route("/get_checkins", methods=["GET"])
def get_checkins():
    conn = get_db()
    data = conn.execute("SELECT * FROM checkin ORDER BY id DESC").fetchall()
    conn.close()

    return jsonify([dict(row) for row in data])

# -------------------------
# ADD MEDICINE
# -------------------------
@app.route("/add_medicine", methods=["POST"])
def add_medicine():
    data = request.json

    name = data.get("name")
    dosage = data.get("dosage")
    time_med = data.get("time")

    conn = get_db()
    conn.execute(
        "INSERT INTO medicine (name,dosage,time) VALUES (?,?,?)",
        (name, dosage, time_med)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Medicine added"})

# -------------------------
# GET MEDICINES
# -------------------------
@app.route("/get_medicines", methods=["GET"])
def get_medicines():
    conn = get_db()
    data = conn.execute("SELECT * FROM medicine").fetchall()
    conn.close()

    return jsonify([dict(row) for row in data])

# -------------------------
# ADD CONTACT
# -------------------------
@app.route("/add_contact", methods=["POST"])
def add_contact():
    data = request.json

    name = data.get("name")
    relation = data.get("relation")
    phone = data.get("phone")

    conn = get_db()
    conn.execute(
        "INSERT INTO contacts (name,relation,phone) VALUES (?,?,?)",
        (name, relation, phone)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Contact added"})

# -------------------------
# GET CONTACTS
# -------------------------
@app.route("/get_contacts", methods=["GET"])
def get_contacts():
    conn = get_db()
    data = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()

    return jsonify([dict(row) for row in data])

# -------------------------
# SOS ALERT
# -------------------------
@app.route("/sos", methods=["POST"])
def sos():
    data = request.json

    location = data.get("location", "Unknown")
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    conn.execute(
        "INSERT INTO sos_alerts (alert_time,location,status) VALUES (?,?,?)",
        (time_now, location, "sent")
    )
    conn.commit()
    conn.close()

    print(f"🚨 SOS TRIGGERED at {location}")

    return jsonify({"message": "SOS alert sent"})

# -------------------------
# LOCATION UPDATE
# -------------------------
@app.route("/location", methods=["POST"])
def location():
    data = request.json

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    conn.execute(
        "INSERT INTO location (latitude,longitude,time) VALUES (?,?,?)",
        (latitude, longitude, time_now)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Location saved"})

# -------------------------
# GET LOCATION
# -------------------------
@app.route("/get_location", methods=["GET"])
def get_location():
    conn = get_db()
    data = conn.execute(
        "SELECT * FROM location ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.close()

    if data:
        return jsonify(dict(data))
    else:
        return jsonify({"message": "No location found"})

# -------------------------
# QUICK CALL
# -------------------------
@app.route("/call", methods=["POST"])
def call():
    number = request.json.get("number")
    return jsonify({"message": f"Calling {number}"})

# -------------------------
# EMERGENCY CALL
# -------------------------
@app.route("/emergency_call", methods=["GET"])
def emergency_call():
    return jsonify({"number": "108"})  # Ambulance India

# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    app.run(debug=True)