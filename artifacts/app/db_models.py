# SQLAlchemy Models
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Create the declarative base class
Base = declarative_base()

# User model mapping to 'users' table
class User(Base):
    __tablename__ = 'users'
    
    # Primary key column
    id = Column(Integer, primary_key=True, index=True)
    # Required text fields with constraints
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    role = Column(Text, nullable=False)
    
    # One-to-many relationship with OnboardingTask
    onboarding_tasks = relationship("OnboardingTask", back_populates="user", cascade="all, delete-orphan")

# OnboardingTask model mapping to 'onboarding_tasks' table
class OnboardingTask(Base):
    __tablename__ = 'onboarding_tasks'
    
    # Primary key column
    id = Column(Integer, primary_key=True, index=True)
    # Task details columns
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)  # Nullable by default, explicit for clarity
    due_date = Column(Date, nullable=True)
    status = Column(Text, nullable=False)
    
    # Foreign key to users table
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    # Many-to-one relationship with User
    user = relationship("User", back_populates="onboarding_tasks")

# Database Session Management
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL pointing to local file
SQLALCHEMY_DATABASE_URL = "sqlite:///./onboarding.db"

# Create SQLAlchemy engine with SQLite-specific connection args
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite to work with multiple threads
)

# Create declarative base if not imported from models
Base = declarative_base()

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI dependency to get database session
def get_db():
    """
    Database session dependency for FastAPI endpoints.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()