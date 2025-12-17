from fastapi import status

from app.services import auth_email


def test_register_and_login_success(client):
    email = "user@example.com"
    password = "StrongPass123!"
    register_payload = {
        "email": email,
        "phone": "+15551234567",
        "password": password,
        "first_name": "Test",
        "last_name": "User",
        "role": "rider",
    }

    resp = client.post("/api/v1/auth/register", json=register_payload)
    assert resp.status_code == status.HTTP_201_CREATED, resp.text
    data = resp.json()
    assert data["email"] == email
    assert data["is_active"] is True
    assert data["is_verified"] is False

    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_resp.status_code == status.HTTP_200_OK, login_resp.text
    tokens = login_resp.json()
    assert tokens["token_type"] == "bearer"
    assert tokens["access_token"]
    assert tokens["refresh_token"]


def test_register_duplicate_email_rejected(client):
    email = "dup@example.com"
    payload = {
        "email": email,
        "phone": None,
        "password": "StrongPass123!",
        "first_name": "First",
        "last_name": "User",
        "role": "rider",
    }

    first = client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == status.HTTP_201_CREATED

    second = client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == status.HTTP_400_BAD_REQUEST
    assert second.json()["detail"] == "Email already registered"


def test_password_reset_flow(client, fake_redis, monkeypatch):
    email = "reset@example.com"
    password = "StrongPass123!"
    register_payload = {
        "email": email,
        "phone": "+15557654321",
        "password": password,
        "first_name": "Reset",
        "last_name": "User",
        "role": "rider",
    }

    register = client.post("/api/v1/auth/register", json=register_payload)
    assert register.status_code == status.HTTP_201_CREATED

    token = "reset-token-123"
    captured: dict[str, str] = {}

    def fake_create_password_reset(user):
        auth_email.store_password_reset_token(user, token)
        return token

    def fake_send_password_reset_email(user, token_value):
        captured["token"] = token_value

    monkeypatch.setattr(auth_email, "create_password_reset_token", fake_create_password_reset)
    monkeypatch.setattr(auth_email, "send_password_reset_email", fake_send_password_reset_email)

    resp = client.post("/api/v1/auth/forgot-password", json={"email": email})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["message"].startswith("If an account exists")
    assert captured["token"] == token
    assert fake_redis.get(f"password_reset:{token}") is not None

    validate = client.post("/api/v1/auth/validate-reset-token", json={"token": token})
    assert validate.status_code == status.HTTP_200_OK
    assert validate.json()["message"] == "Token is valid"

    new_password = "NewPass456!"
    reset_resp = client.post(
        "/api/v1/auth/reset-password", json={"token": token, "new_password": new_password}
    )
    assert reset_resp.status_code == status.HTTP_200_OK
    assert reset_resp.json()["message"] == "Password has been reset successfully"
    assert fake_redis.get(f"password_reset:{token}") is None

    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": new_password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_resp.status_code == status.HTTP_200_OK
    tokens = login_resp.json()
    assert tokens["access_token"]
    assert tokens["refresh_token"]


def test_validate_reset_token_rejects_invalid(client):
    resp = client.post("/api/v1/auth/validate-reset-token", json={"token": "nope"})
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json()["detail"] == "Invalid or expired token"
