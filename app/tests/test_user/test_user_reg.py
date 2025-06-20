from tests.conftest import USER_NAME, USER_EMAIL, USER_PASSWORD
from app_tools.models.user import User

user_data = {
            "name": USER_NAME,
            "email": USER_EMAIL,
            "password": USER_PASSWORD,
        }


def test_create_user(client, db_session):
    # Test user creation
    response = client.post(
        "/users/sign_up",
        json=user_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["name"] == USER_NAME
    assert data["user"]["email"] == USER_EMAIL
    assert "password" not in data
    assert data["user"]["is_active"] is False
    assert data["user"]["is_verified"] is False
    db_user = db_session.query(User).filter(
        User.email == data["user"]["email"]).first()
    assert db_user.is_verified is False
    assert db_user.is_active is False


def test_create_user_with_existing_mail(client, user_sample):
    new_user_data = user_data.copy()
    new_user_data["name"] = "Elis Okonkwo"
    response = client.post("/users/sign_up", json=new_user_data)

    assert response.status_code != 201
    assert response.status_code == 400
    assert response.json() == {"detail": "This email exists in database."}


def test_create_user_with_invalid_mail(client):
    new_user_data = user_data.copy()
    new_user_data["email"] = "elisis.com"
    response = client.post("/users/sign_up", json=new_user_data)

    assert response.status_code != 201
    assert response.status_code == 422


def test_create_user_without_pwd(client):
    new_user_data = user_data.copy()
    new_user_data["password"] = None
    print(new_user_data)

    response = client.post("/users/sign_up", json=new_user_data)

    assert response.status_code != 201
    assert response.status_code == 422


def create_user_with_num_pwd(client):
    new_user_data = user_data.copy()
    new_user_data["password"] = 1234567
    print(new_user_data)

    response = client.post("/users/sign_up", json=new_user_data)

    assert response.status_code != 201
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Password must be at least 7 characters long, "
                  "contain at least one digit, one lowercase letter, "
                  "and one uppercase letter."
    }


def create_user_with_alpha_pwd(client):
    new_user_data = user_data.copy()
    new_user_data["password"] = "Noneada"
    print(new_user_data)

    response = client.post("/users/sign_up", json=new_user_data)

    assert response.status_code != 201
    assert response.status_code == 400
