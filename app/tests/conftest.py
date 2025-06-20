from datetime import datetime
import os
import sys
from typing import Generator
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from main import app
from app_tools.core.db.database import Base, get_session
from app_tools.core.security import security
from app_tools.models.user import User

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)

USER_NAME = "Ada Okonkwo"
USER_EMAIL = "dovedrops4@gmail.com"
USER_PASSWORD = "aDaX123"

# Recreate database engine to use SQLite for testing
test_engine = create_engine(
    "sqlite:///./testing.db", connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)


# Fixture to use test DB session inside test functions
@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create the database and destroy it after the tests
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# Fixture to create FastAPI test client with overridden session
@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    def _override_get_session():
        # Create a new database session for testing.
        yield db_session
    app.dependency_overrides[get_session] = _override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# Fixture to create a test user in the database
@pytest.fixture(scope="function")
def user_sample():
    db = TestingSessionLocal()
    test_user = User(
        name=USER_NAME,
        email=USER_EMAIL,
        password=security.hash_password(USER_PASSWORD)
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    # session.close()
    return test_user


@pytest.fixture(scope="function")
def user_with_token(client, user_sample):
    # Create a test user and generate a token for them
    user = user_sample
    token = security.generate_token(data={"id": user.id, "email": user.email})
    return user, token


@pytest.fixture(scope="function")
def verified_user():
    db = TestingSessionLocal()
    test_user = User(
        name=USER_NAME,
        email=USER_EMAIL,
        password=security.hash_password(USER_PASSWORD),
        is_active=True,
        is_verified=True,
        verified_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    # session.close()
    return test_user


@pytest.fixture(scope="function")
def inactive_user():
    db = TestingSessionLocal()
    test_user = User(
        name=USER_NAME,
        email=USER_EMAIL,
        password=security.hash_password(USER_PASSWORD),
        is_active=False,
        is_verified=True,
        verified_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    # session.close()
    return test_user
