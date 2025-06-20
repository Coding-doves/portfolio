from datetime import datetime
import jwt

from app_tools.core.config import Settings
from tests.conftest import USER_PASSWORD

settings = Settings()


def test_user_signin(client, verified_user, db_session):
    response = client.post(
        "/users/signin",
        data={
            'username': verified_user.email,
            'password': USER_PASSWORD
        }
    )

    assert response.status_code == 200
    res = response.json()
    assert res['access_token'] is not None
    assert res['refresh_token'] is not None
    assert res['expires_in'] is not None


def test_signin_with_wrong_pwd(client, verified_user):
    response = client.post(
        "/users/signin",
        data={
            'username': verified_user.email,
            'password': 'wrong_PASSWORD'
        }
    )

    assert response.status_code == 400
    response.json()['detail'] == 'Incorrect email or password'


def test_signin_with_wrong_email(client, verified_user):
    response = client.post(
        "/users/signin",
        data={
            'username': 'dovedrop@gmail.com',
            'password': USER_PASSWORD
        }
    )

    assert response.status_code == 400
    response.json()['detail'] == 'Incorrect email or password'


def test_signin_for_inactive_user(client, inactive_user):
    response = client.post(
        "/users/signin",
        data={
            'username': inactive_user.email,
            'password': USER_PASSWORD
        }
    )
    assert response.status_code == 400


def test_signin_for_unverified_user(client, user_sample):
    response = client.post(
        "/users/signin",
        data={
            'username': user_sample.email,
            'password': USER_PASSWORD
        }
    )
    assert response.status_code == 400
    
    
def test_access_token_generation_for_verified_user(client, verified_user, db_session):
    response = client.post(
        "/users/signin",
        data={
            'username': verified_user.email,
            'password': USER_PASSWORD
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access" in data

    # Decode access token
    decoded = jwt.decode(
        data["access_token"],
        settings.SECRET_KEY,
        algorithms=["HS256"]
    )
    assert decoded["email"] == verified_user.email


def test_refresh_token_generation_for_verified_user(client, verified_user):
    response = client.post(
        "/users/signin",
        data={
            'username': verified_user.email,
            'password': USER_PASSWORD
        }
    )

    data = response.json()
    assert "refresh_token" in data

    # Decode refresh token
    decoded = jwt.decode(
        data["refresh_token"],
        settings.SECRET_KEY,
        algorithms=["HS256"]
    )
    print(decoded)
    assert decoded["email"] == verified_user.email


def test_token_expiry_for_verified_user(client, verified_user):
    response = client.post(
        "/users/signin",
        data={
            'username': verified_user.email,
            'password': USER_PASSWORD
        }
    )
    data = response.json()
    decoded = jwt.decode(
        data["access_token"],
        settings.SECRET_KEY,
        algorithms=["HS256"]
    )
    exp_timestamp = decoded["exp"]
    exp_time = datetime.utcfromtimestamp(exp_timestamp)
    assert exp_time > datetime.utcnow()

    """
    test resend email
    """