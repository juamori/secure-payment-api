import os
import sqlite3

def get_db_path() -> str:
    return os.getenv("DB_PATH", "secure_payments.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn
