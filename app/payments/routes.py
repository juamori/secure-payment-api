import logging
from flask import Blueprint, request, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError

from app.payments.schemas import PaymentCreate
from app.payments.service import create_payment, get_payment

logger = logging.getLogger(__name__)

payments_bp = Blueprint("payments", __name__)

@payments_bp.route("", methods=["POST"])
@jwt_required()
def create():
    owner = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    try:
        payload = PaymentCreate(**data).model_dump()
    except ValidationError as e:
        logger.info("payment_validation_error", extra={
            "request_id": getattr(g, "request_id", None),
            "method": "POST",
            "path": "/payments",
            "status_code": 400,
        })
        return {"error": "validation_error", "details": e.errors()}, 400

    payment = create_payment(owner=owner, payload=payload)

    logger.info("payment_created", extra={
        "request_id": getattr(g, "request_id", None),
        "method": "POST",
        "path": "/payments",
        "status_code": 201,
        "payment_id": payment.get("id"),
        "owner": owner,
    })

    return payment, 201

@payments_bp.route("/<payment_id>", methods=["GET"])
@jwt_required()
def get_one(payment_id: str):
    owner = get_jwt_identity()
    payment = get_payment(owner=owner, payment_id=payment_id)
    if not payment:
        logger.info("payment_not_found_or_forbidden", extra={
            "request_id": getattr(g, "request_id", None),
            "method": "GET",
            "path": f"/payments/{payment_id}",
            "status_code": 404,
            "owner": owner,
        })
        return {"error": "not_found"}, 404

    return payment, 200
