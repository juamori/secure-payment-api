from app import create_app

def _login(client, username="julia"):
    resp = client.post("/auth/login", json={"username": username, "password": "123"})
    assert resp.status_code == 200
    return resp.get_json()["access_token"]

def test_payments_requires_auth():
    app = create_app()
    client = app.test_client()

    resp = client.post("/payments", json={})
    assert resp.status_code in (401, 422)

def test_create_payment_and_idempotency():
    app = create_app()
    client = app.test_client()

    token = _login(client, "julia")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "amount_cents": 1990,
        "currency": "BRL",
        "payer": {"name": "Julia Amorim", "document": "12345678900"},
        "description": "pytest payment",
        "idempotency_key": "pytest-idem-1",
    }

    r1 = client.post("/payments", json=payload, headers=headers)
    assert r1.status_code == 201
    p1 = r1.get_json()

    assert "id" in p1
    assert p1["payer"]["document"].endswith("8900")
    assert "document_encrypted" not in p1["payer"]

    r2 = client.post("/payments", json=payload, headers=headers)
    assert r2.status_code == 201
    p2 = r2.get_json()

    assert p2["id"] == p1["id"]

def test_owner_access_control():
    app = create_app()
    client = app.test_client()

    token_julia = _login(client, "julia")
    headers_julia = {"Authorization": f"Bearer {token_julia}"}

    payload = {
        "amount_cents": 2500,
        "currency": "BRL",
        "payer": {"name": "Julia Amorim", "document": "12345678900"},
        "description": "owner test",
        "idempotency_key": "pytest-idem-owner-1",
    }

    created = client.post("/payments", json=payload, headers=headers_julia)
    assert created.status_code == 201
    pid = created.get_json()["id"]

    token_intruso = _login(client, "intruso")
    headers_intruso = {"Authorization": f"Bearer {token_intruso}"}

    denied = client.get(f"/payments/{pid}", headers=headers_intruso)
    assert denied.status_code == 404
