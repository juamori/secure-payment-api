from app import create_app

def test_health():
    app = create_app()
    client = app.test_client()

    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

def test_login_returns_token():
    app = create_app()
    client = app.test_client()

    resp = client.post("/auth/login", json={"username": "julia", "password": "123"})
    assert resp.status_code == 200

    data = resp.get_json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20
