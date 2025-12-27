import sqlite3
from pathlib import Path

DB_PATH = Path("database/voters.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voters (
        voter_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        embedding BLOB NOT NULL,
        has_voted INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database initialized")

import numpy as np

def insert_voter(name, embedding):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO voters (name, embedding, has_voted) VALUES (?, ?, 0)",
        (name, embedding.tobytes())
    )

    conn.commit()
    conn.close()

def get_all_voters():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT voter_id, name, embedding, has_voted FROM voters")
    rows = cursor.fetchall()

    conn.close()

    voters = []
    for voter_id, name, emb_blob, has_voted in rows:
        emb = np.frombuffer(emb_blob, dtype=np.float32)
        voters.append((voter_id, name, emb, has_voted))

    return voters
def mark_voted(voter_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE voters SET has_voted = 1 WHERE voter_id = ?",
        (voter_id,)
    )

    conn.commit()
    conn.close()
def reset_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM voters")

    conn.commit()
    conn.close()
