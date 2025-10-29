"""FastAPI application backed by SQLite for Day 3 Challenge 3."""
from __future__ import annotations

from datetime import datetime
from typing import Generator, List, Literal, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

DATABASE_URL = "sqlite:///artifacts/onboarding.db"


class Base(DeclarativeBase):
    """Declarative base for ORM models."""


class Company(Base):
    __tablename__ = "companies"

    company_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    users: Mapped[list["User"]] = relationship("User", back_populates="company", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(Enum("Admin", "Hiring Manager", "New Hire"), nullable=False)
    manager_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    company: Mapped["Company"] = relationship("Company", back_populates="users")
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="uploaded_by", foreign_keys="Document.uploaded_by_user_id")
    managed_users: Mapped[list["User"]] = relationship("User", back_populates="manager", foreign_keys=[manager_id])
    manager: Mapped[Optional["User"]] = relationship("User", remote_side=[user_id], back_populates="managed_users")
    onboarding_plans: Mapped[list["OnboardingPlan"]] = relationship("OnboardingPlan", back_populates="created_by", foreign_keys="OnboardingPlan.created_by_user_id")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="user")
    onboarding_processes: Mapped[list["OnboardingProcess"]] = relationship("OnboardingProcess", back_populates="new_hire", foreign_keys="OnboardingProcess.new_hire_user_id")
    managed_onboarding_processes: Mapped[list["OnboardingProcess"]] = relationship("OnboardingProcess", back_populates="hiring_manager", foreign_keys="OnboardingProcess.hiring_manager_user_id")


class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    file_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    uploaded_by_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    company: Mapped["Company"] = relationship("Company")
    uploaded_by: Mapped[Optional["User"]] = relationship("User", back_populates="documents")


class OnboardingPlan(Base):
    __tablename__ = "onboarding_plans"

    plan_id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_by_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    company: Mapped["Company"] = relationship("Company")
    created_by: Mapped[Optional["User"]] = relationship("User", back_populates="onboarding_plans")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="plan", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("onboarding_plans.plan_id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    due_days_after_start: Mapped[int] = mapped_column(nullable=False)
    order_in_plan: Mapped[int] = mapped_column(nullable=False)
    document_id: Mapped[Optional[int]] = mapped_column(ForeignKey("documents.document_id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    plan: Mapped["OnboardingPlan"] = relationship("OnboardingPlan", back_populates="tasks")
    document: Mapped[Optional["Document"]] = relationship("Document")
    assigned_tasks: Mapped[list["AssignedTask"]] = relationship("AssignedTask", back_populates="task", cascade="all, delete-orphan")


class OnboardingProcess(Base):
    __tablename__ = "onboarding_processes"

    process_id: Mapped[int] = mapped_column(primary_key=True)
    new_hire_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    plan_id: Mapped[int] = mapped_column(ForeignKey("onboarding_plans.plan_id", ondelete="RESTRICT"), nullable=False)
    hiring_manager_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(Enum("Not Started", "In Progress", "Completed"), default="Not Started", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    new_hire: Mapped["User"] = relationship("User", back_populates="onboarding_processes", foreign_keys=[new_hire_user_id])
    hiring_manager: Mapped["User"] = relationship("User", back_populates="managed_onboarding_processes", foreign_keys=[hiring_manager_user_id])
    plan: Mapped["OnboardingPlan"] = relationship("OnboardingPlan")
    assigned_tasks: Mapped[list["AssignedTask"]] = relationship("AssignedTask", back_populates="process", cascade="all, delete-orphan")


class AssignedTask(Base):
    __tablename__ = "assigned_tasks"

    assigned_task_id: Mapped[int] = mapped_column(primary_key=True)
    process_id: Mapped[int] = mapped_column(ForeignKey("onboarding_processes.process_id", ondelete="CASCADE"), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.task_id", ondelete="RESTRICT"), nullable=False)
    status: Mapped[str] = mapped_column(Enum("Pending", "Completed"), default="Pending", nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    process: Mapped["OnboardingProcess"] = relationship("OnboardingProcess", back_populates="assigned_tasks")
    task: Mapped["Task"] = relationship("Task", back_populates="assigned_tasks")


class Notification(Base):
    __tablename__ = "notifications"

    notification_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="notifications")


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# Ensure tables exist for workshop runtimes that bootstrap an empty database.
Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserBase(BaseModel):
    company_id: int = Field(..., ge=1)
    email: EmailStr
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    role: Literal["Admin", "Hiring Manager", "New Hire"]
    manager_id: Optional[int] = Field(default=None, ge=1)


class UserCreate(UserBase):
    password_hash: str = Field(..., min_length=1)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[Literal["Admin", "Hiring Manager", "New Hire"]] = None
    manager_id: Optional[int] = Field(default=None, ge=1)
    password_hash: Optional[str] = Field(default=None, min_length=1)

    model_config = ConfigDict(extra="forbid")


class UserOut(UserBase):
    user_id: int
    password_hash: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


app = FastAPI(title="Onboarding SQLite API")


def ensure_email_unique(db: Session, email: str, *, exclude_user_id: Optional[int] = None) -> None:
    conditions = [User.email == email]
    if exclude_user_id is not None:
        conditions.append(User.user_id != exclude_user_id)
    existing = db.execute(select(User).where(*conditions)).scalars().first()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")


def ensure_manager_valid(db: Session, manager_id: Optional[int], *, for_user_id: Optional[int] = None) -> None:
    if manager_id is None:
        return
    if for_user_id is not None and manager_id == for_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User cannot manage themselves")
    if db.get(User, manager_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Manager not found")


@app.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)) -> List[UserOut]:
    users = db.execute(select(User).order_by(User.user_id)).scalars().all()
    return [UserOut.model_validate(user) for user in users]


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserOut:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut.model_validate(user)


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    ensure_email_unique(db, payload.email)
    ensure_manager_valid(db, payload.manager_id)

    user = User(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)) -> UserOut:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_data = payload.model_dump(exclude_unset=True)
    new_email = update_data.get("email")
    if new_email is not None:
        ensure_email_unique(db, new_email, exclude_user_id=user_id)

    if "manager_id" in update_data:
        ensure_manager_valid(db, update_data["manager_id"], for_user_id=user_id)

    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
