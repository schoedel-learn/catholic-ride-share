from fastapi import status


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
