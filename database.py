import sqlite3

# connect to database
conn = sqlite3.connect("elderwatch.db")
cursor = conn.cursor()

# -----------------------------
# CHECK-IN TABLE
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS checkin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT,
    time TEXT
)
""")

# -----------------------------
# MEDICINE TABLE
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS medicine (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dosage TEXT,
    time TEXT
)
""")

# -----------------------------
# CONTACTS TABLE
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    relation TEXT,
    phone TEXT
)
""")

# -----------------------------
# SOS ALERT TABLE
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS sos_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_time TEXT,
    location TEXT,
    status TEXT
)
""")

# -----------------------------
# LOCATION TABLE
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL,
    longitude REAL,
    time TEXT
)
""")

# save and close
conn.commit()
conn.close()

print("ElderWatch database created successfully!")