from app.db.database import get_connection

def init_db():
    conn = get_connection()
    try:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id TEXT PRIMARY KEY,
            owner TEXT NOT NULL,
            amount_cents INTEGER NOT NULL,
            currency TEXT NOT NULL,
            payer_name TEXT NOT NULL,
            payer_document_masked TEXT NOT NULL,
            payer_document_encrypted TEXT NOT NULL,
            description TEXT,
            idempotency_key TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL,
            created_at INTEGER NOT NULL
        );
        """)
        conn.commit()
    finally:
        conn.close()
