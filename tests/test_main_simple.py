# test_main.py
# To run these tests, save the provided FastAPI app as `main.py`
# and this file as `test_main.py` in the same directory.
# Then run `pytest` from your terminal.

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import the main FastAPI application and dependency
from app.main import app, Base, get_db

# --- Test Database Setup ---

# Use an in-memory SQLite database for isolated testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args is needed only for SQLite
    connect_args={"check_same_thread": False},
    # StaticPool is used to ensure the same connection is used for the lifespan
    # of the test, which is important for in-memory databases.
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Dependency Override ---

# This function will override the `get_db` dependency in the main app
# to ensure that the test database is used during tests.
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Apply the dependency override to the app
app.dependency_overrides[get_db] = override_get_db


# --- Pytest Fixtures ---


@pytest.fixture()
def client():
    """
    A fixture to set up and tear down the database for each test function.
    It creates all database tables before a test runs and drops them afterward,
    ensuring a clean state for each test.
    """
    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)
    # Yield a TestClient instance for making requests to the app
    yield TestClient(app)
    # Drop all tables after the test is complete
    Base.metadata.drop_all(bind=engine)


# --- Tests ---


def test_create_user(client: TestClient):
    """
    Test the user creation endpoint (POST /users/).
    - Asserts that the status code is 201 (Created).
    - Asserts that the response body contains the correct email and an 'id'.
    """
    response = client.post(
        "/users/",
        json={"name": "Test User", "email": "testuser@example.com", "role": "employee"},
    )
    data = response.json()

    assert response.status_code == 201
    assert data["email"] == "testuser@example.com"
    assert "id" in data
    # Ensure the password is not returned in the response
    assert "password" not in data


def test_read_users(client: TestClient):
    """
    Test the endpoint for reading a list of all users (GET /users/).
    - First, creates a user to ensure the database is not empty.
    - Asserts that the status code is 200 (OK).
    - Asserts that the response is a list.
    - Asserts that the created user is present in the list.
    """
    # 1. Create a user to ensure the list is not empty
    user_payload = {"name": "User One", "email": "user1@example.com", "role": "employee"}
    create_response = client.post("/users/", json=user_payload)
    assert create_response.status_code == 201
    created_user_data = create_response.json()

    # 2. Test the GET endpoint to read all users
    response = client.get("/users/")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    # The list should contain the user we just created
    assert len(data) > 0
    # Check if the created user's data is in the list
    assert created_user_data in data