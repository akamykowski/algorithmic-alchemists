from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import User


def test_create_user(client: TestClient, db_session: Session):
    """
    Test creating a user successfully.
    """
    response = client.post(
        "/users/",
        json={"name": "Test User", "email": "test@example.com", "role": "employee"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

    # Verify the user was actually created in the database
    user_in_db = db_session.query(User).filter(User.id == data["id"]).first()
    assert user_in_db is not None
    assert user_in_db.email == "test@example.com"


def test_read_users(client: TestClient, db_session: Session):
    """
    Test reading a list of users.
    """
    # Create some users directly in the test database
    user1 = User(name="User One", email="user1@example.com", role="employee")
    user2 = User(name="User Two", email="user2@example.com", role="manager")
    db_session.add_all([user1, user2])
    db_session.commit()

    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["email"] == "user1@example.com"
    assert data[1]["email"] == "user2@example.com"


def test_read_user(client: TestClient, db_session: Session):
    """
    Test reading a single user by their ID.
    """
    # Create a user directly in the test database to fetch
    test_user = User(name="Specific User", email="specific.user@example.com", role="employee")
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email