import pytest
from fastapi.testclient import TestClient
from fastapi_email.main import app
from fastapi_email.database import Base, get_db, engine
from fastapi_email.models import User
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

# Use same engine as app, but with isolated session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override dependency
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# ✅ Reset the database before each test
@pytest.fixture(autouse=True)
def reset_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@patch("fastapi_email.main.send_verification_email", return_value=None)
@patch("fastapi_email.main.send_confirmation_email", return_value=None)
def test_register_new_email(mock_confirm, mock_verify):
    response = client.post("/register", json={"email": "abhi.playstore65@gmail.com"})
    assert response.status_code == 200
    assert "Verification email sent" in response.json()["message"]


@patch("fastapi_email.main.send_verification_email", return_value=None)
@patch("fastapi_email.main.send_confirmation_email", return_value=None)
def test_duplicate_unverified_registration(mock_confirm, mock_verify):
    client.post("/register", json={"email": "test.user2@example.com"})  # first call
    response = client.post("/register", json={"email": "test.user2@example.com"})  # second call
    assert response.status_code == 200
    assert "Verification email re-sent" in response.json()["message"]


def test_status_check_unverified():
    client.post("/register", json={"email": "test.user3@example.com"})
    response = client.get("/status/test.user3@example.com")
    assert response.status_code == 200
    assert response.json()["is_verified"] is False


@patch("fastapi_email.main.send_verification_email", return_value=None)
@patch("fastapi_email.main.send_confirmation_email", return_value=None)
def test_verification_flow(mock_confirm, mock_verify):
    client.post("/register", json={"email": "test.user4@example.com"})

    # Access token from DB
    db = next(override_get_db())
    user = db.query(User).filter(User.email == "test.user4@example.com").first()
    token = user.token

    verify_response = client.get(f"/verify/{token}")
    assert verify_response.status_code == 200
    assert "Email verified" in verify_response.json()["message"]

    # Confirm status
    status_response = client.get("/status/test.user4@example.com")
    assert status_response.status_code == 200
    assert status_response.json()["is_verified"] is True


@patch("fastapi_email.main.send_verification_email", return_value=None)
@patch("fastapi_email.main.send_confirmation_email", return_value=None)
def test_duplicate_verified_registration_fails(mock_confirm, mock_verify):
    client.post("/register", json={"email": "test.user5@example.com"})

    db = next(override_get_db())
    user = db.query(User).filter(User.email == "test.user5@example.com").first()
    user.is_verified = True
    db.commit()

    response = client.post("/register", json={"email": "test.user5@example.com"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already verified"
