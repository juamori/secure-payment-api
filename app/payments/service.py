import time
import uuid

from app.db.database import get_connection
from app.common.security import encrypt_str, mask_document

def _row_to_public_payment(row) -> dict:
    return {
        "id": row["id"],
        "status": row["status"],
        "created_at": row["created_at"],
        "owner": row["owner"],
        "amount_cents": row["amount_cents"],
        "currency": row["currency"],
        "payer": {
            "name": row["payer_name"],
            "document": row["payer_document_masked"],
        },
        "description": row["description"],
        "idempotency_key": row["idempotency_key"],
    }

def create_payment(owner: str, payload: dict) -> dict:
    idem_key = payload["idempotency_key"]

    conn = get_connection()
    try:
        existing = conn.execute(
            "SELECT * FROM payments WHERE idempotency_key = ?",
            (idem_key,)
        ).fetchone()

        if existing:
            return _row_to_public_payment(existing)

        payment_id = str(uuid.uuid4())
        now = int(time.time())

        payer_name = payload["payer"]["name"]
        payer_doc = payload["payer"]["document"]           
        payer_doc_masked = mask_document(payer_doc)
        payer_doc_encrypted = encrypt_str(payer_doc)

        conn.execute(
            """
            INSERT INTO payments (
                id, owner, amount_cents, currency,
                payer_name, payer_document_masked, payer_document_encrypted,
                description, idempotency_key, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payment_id, owner, payload["amount_cents"], payload["currency"],
                payer_name, payer_doc_masked, payer_doc_encrypted,
                payload.get("description"), idem_key, "CREATED", now
            )
        )
        conn.commit()

        row = conn.execute("SELECT * FROM payments WHERE id = ?", (payment_id,)).fetchone()
        return _row_to_public_payment(row)

    finally:
        conn.close()

def get_payment(owner: str, payment_id: str) -> dict | None:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM payments WHERE id = ? AND owner = ?",
            (payment_id, owner)
        ).fetchone()

        if not row:
            return None

        return _row_to_public_payment(row)
    finally:
        conn.close()
