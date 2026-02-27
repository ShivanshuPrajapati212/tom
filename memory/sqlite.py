from datetime import datetime
import sqlite3


conn = sqlite3.connect("long_term_memory.db")
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        summary TEXT NOT NULL,
        importance REAL,
        created_at TEXT
    )
""")
conn.commit()
def add_to_db(event_type, summary, importance):
    conn = sqlite3.connect("long_term_memory.db")
    cursor = conn.cursor()
    now = datetime.now().isoformat()  # "2026-02-26T14:30:00.123456"
    cursor.execute("INSERT INTO events (event_type, summary, importance, created_at) VALUES (?, ?, ?, ?)", (event_type, summary, importance, now))
    conn.commit()

def get_all_rows():
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    return rows

if __name__ == "__main__":
    get_all_rows()
