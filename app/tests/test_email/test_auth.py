from fastapi import BackgroundTasks
from app_tools.core.email import send_email
from app_tools.models.user import User


def test_email(user_with_token):
    # Test email sending
    email_response = send_email(
        receiver=user_with_token[0],
        subject="Verify Email",
        context={},
        template_name="verify_email.html",
        background_tasks=BackgroundTasks(),
    )
    assert email_response is None


def test_user_verification(client, user_with_token):
    # Test user verification
    user, token = user_with_token

    # First call should verify user successfully
    response = client.get(f"/auth/verification/?token={token}")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert f"Hello {user.name}" in response.text
    assert "successfully verified" in response.text

    # Second call: already verified
    response = client.get(f"/auth/verification/?token={token}")
    assert response.status_code == 200
    assert "already verified" in response.text


def test_user_verification_api(client, user_with_token, db_session):
    # Test user verification
    user, token = user_with_token

    # First call should verify user successfully
    response = client.get(f"/auth/verification_API/?token={token}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["name"] == user.name
    db_user = db_session.query(User).filter(User.id == user.id).first()
    assert db_user.is_verified is True
    assert db_user.is_active is True

    # Second call: already verified
    response = client.get(f"/auth/verification_API/?token={token}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "already_verified"
    assert data["name"] == user.name


def test_invalid_verification_token(client, user_sample, db_session):
    # Invalid token
    response = client.get("/auth/verification/?token=invalid_token")
    assert response.status_code == 200
    assert "Verification Failed" in \
        response.text or "Token has expired" in response.text

    # Invalid token for API
    response = client.get("/auth/verification_API/?token=invalid_token")
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] in [
        "Invalid token", "Token has expired or is invalid"]
    db_user = db_session.query(User).filter(User.id == user_sample.id).first()
    assert db_user.is_verified is False
    assert db_user.is_active is False


def test_invalid_email_verification(client, user_with_token):
    pass
