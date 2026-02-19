import sqlite3
import datetime
import json

DB_PATH = "custody/custodian_ledger.db"

def connect():
    return sqlite3.connect(DB_PATH)

def write_record(event_type, payload):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ledger(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_type TEXT,
            payload TEXT
        )
    """)
    conn.commit()

    timestamp = datetime.datetime.now().isoformat()
    payload_json = json.dumps(payload, ensure_ascii=False, default=str)
    cursor.execute(
        "INSERT INTO ledger (timestamp, event_type, payload) VALUES (?, ?, ?)",
        (timestamp, event_type, payload_json),
    )
    conn.commit()
    conn.close()
