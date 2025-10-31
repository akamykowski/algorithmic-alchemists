# conftest.py

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import from app.main (FastAPI application)
from app.main import app, Base, get_db

# --- Database Setup for Testing ---

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create a SQLAlchemy engine for the test database
# connect_args is needed for SQLite to allow multi-threaded access
# StaticPool is used to ensure the same connection is used for the lifespan of the test
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create a sessionmaker for the test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Fixture Definition ---

@pytest.fixture(scope="function")
def client():
    """
    Pytest fixture to provide an isolated database session and a TestClient for each test function.
    """
    # Create all database tables before running a test
    Base.metadata.create_all(bind=engine)

    # Define a dependency override for get_db
    def override_get_db():
        """
        A dependency override that provides a test database session.
        """
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    # Apply the override to the FastAPI app
    app.dependency_overrides[get_db] = override_get_db

    # Yield the TestClient to the test function
    with TestClient(app) as test_client:
        yield test_client

    # Drop all database tables after the test has run
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Pytest fixture to provide a database session for direct DB operations in tests.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

    # Clear the dependency overrides after the test
    app.dependency_overrides.clear()