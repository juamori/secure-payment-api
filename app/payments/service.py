import time
import uuid
from typing import Dict, Any

from app.common.security import encrypt_str, mask_document

_PAYMENTS: Dict[str, Dict[str, Any]] = {}
_IDEMPOTENCY: Dict[str, str] = {}  

def _public_payment(payment: Dict[str, Any]) -> Dict[str, Any]:
    safe = dict(payment)
    safe_payer = dict(safe.get("payer", {}))
    safe_payer.pop("document_encrypted", None)
    safe["payer"] = safe_payer
    return safe

def create_payment(owner: str, payload: dict) -> dict:
    idem_key = payload["idempotency_key"]

    if idem_key in _IDEMPOTENCY:
        payment_id = _IDEMPOTENCY[idem_key]
        return _public_payment(_PAYMENTS[payment_id])

    payment_id = str(uuid.uuid4())
    now = int(time.time())

    payer = payload["payer"].copy()
    payer["document_encrypted"] = encrypt_str(payer["document"])
    payer["document"] = mask_document(payer["document"])

    payment = {
        "id": payment_id,
        "status": "CREATED",
        "created_at": now,
        "owner": owner,
        "amount_cents": payload["amount_cents"],
        "currency": payload["currency"],
        "payer": payer,
        "description": payload.get("description"),
        "idempotency_key": idem_key,
    }

    _PAYMENTS[payment_id] = payment
    _IDEMPOTENCY[idem_key] = payment_id
    return _public_payment(payment)

def get_payment(owner: str, payment_id: str) -> dict | None:
    payment = _PAYMENTS.get(payment_id)
    if not payment:
        return None
    if payment["owner"] != owner:
        return None
    return _public_payment(payment)
