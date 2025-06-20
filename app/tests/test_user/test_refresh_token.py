from fastapi.testclient import TestClient
from datetime import timedelta, datetime
import jwt

from app.main import app
from app_tools.core.security import security
from app_tools.core.config import Settings

client = TestClient(app)
settings = Settings()

# Utility to generate tokens
def get_token(user_id=1, email="user@example.com", token_type="refresh", expires_in=timedelta(minutes=30)):
    data = {
        "id": user_id,
        "email": email
    }
    return security.generate_token(data=data, token_type=token_type, expires=expires_in)

# Valid refresh token
def test_refresh_token_success():
    refresh_token = get_token()
    headers = {"Authorization": f"Bearer {refresh_token}"}
    response = client.get("/users/refresh_token", headers=headers)

    assert response.status_code == 200
    assert "access_token" in response.json()

# Expired refresh token
def test_refresh_token_expired():
    expired_token = get_token(expires_in=timedelta(seconds=-10))
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/users/refresh_token", headers=headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired token"

# Access token instead of refresh token
def test_access_token_instead_of_refresh():
    access_token = get_token(token_type="access")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/refresh_token", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Please provide a refresh token"

# Malformed token
def test_malformed_token():
    headers = {"Authorization": "Bearer abc.def.ghi"}
    response = client.get("/users/refresh_token", headers=headers)

    assert response.status_code == 403 or response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()

# Missing Authorization header
def test_missing_authorization_header():
    response = client.get("/users/refresh_token")
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid authorization header"

# Empty token in header
def test_empty_token():
    headers = {"Authorization": "Bearer "}
    response = client.get("/users/refresh_token", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid authorization header"
