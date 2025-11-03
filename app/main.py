"""FastAPI application backed by SQLite for Day 3 Challenge 3."""
from __future__ import annotations

import os
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Generator, List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import Date, ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

APP_ROOT = Path(__file__).resolve().parent.parent

_db_path_env = os.getenv("DATABASE_PATH")
if _db_path_env:
    candidate_path = Path(_db_path_env)
    if not candidate_path.is_absolute():
        candidate_path = APP_ROOT / candidate_path
else:
    candidate_path = APP_ROOT / "artifacts" / "onboarding.db"

candidate_path.parent.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = candidate_path
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


class Base(DeclarativeBase):
    """Declarative base for ORM models."""


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)

    tasks: Mapped[List["OnboardingTask"]] = relationship(
        "OnboardingTask",
        back_populates="assignee",
        cascade="all, delete-orphan",
    )


class OnboardingTask(Base):
    __tablename__ = "onboarding_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    assignee: Mapped[Optional[User]] = relationship("User", back_populates="tasks")


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
    name: str = Field(..., min_length=1)
    email: EmailStr
    role: str = Field(..., min_length=1)


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    email: Optional[EmailStr] = None
    role: Optional[str] = Field(default=None, min_length=1)

    model_config = ConfigDict(extra="forbid")


class UserOut(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: str = Field(..., min_length=1)
    user_id: Optional[int] = Field(default=None, ge=1)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = Field(default=None, min_length=1)
    user_id: Optional[int] = Field(default=None, ge=1)

    model_config = ConfigDict(extra="forbid")


class TaskOut(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


app = FastAPI(title="Onboarding SQLite API")


def streamlit_enabled() -> bool:
    """Return True when the Streamlit UI should be launched."""

    return os.getenv("ENABLE_STREAMLIT_UI", "0") == "1"


_STREAMLIT_PROCESS: Optional[subprocess.Popen[str]] = None


@app.on_event("startup")
def launch_streamlit_ui() -> None:
    """Optionally launch the Streamlit HR dashboard in a background process."""

    if not streamlit_enabled():
        return

    global _STREAMLIT_PROCESS
    if _STREAMLIT_PROCESS and _STREAMLIT_PROCESS.poll() is None:
        return

    script_path = Path(__file__).resolve().parent.parent / "frontend" / "hr_dashboard.py"
    if not script_path.exists():
        return

    port = os.getenv("STREAMLIT_PORT", "8501")
    address = os.getenv("STREAMLIT_ADDRESS", "127.0.0.1")
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(script_path),
        "--server.port",
        str(port),
        "--server.address",
        address,
        "--server.headless",
        "true",
    ]

    try:
        _STREAMLIT_PROCESS = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        _STREAMLIT_PROCESS = None


@app.on_event("shutdown")
def shutdown_streamlit_ui() -> None:
    """Terminate the Streamlit process when the API shuts down."""

    global _STREAMLIT_PROCESS
    if _STREAMLIT_PROCESS and _STREAMLIT_PROCESS.poll() is None:
        _STREAMLIT_PROCESS.terminate()
        try:
            _STREAMLIT_PROCESS.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _STREAMLIT_PROCESS.kill()
    _STREAMLIT_PROCESS = None


def ensure_email_unique(db: Session, email: str, *, exclude_user_id: Optional[int] = None) -> None:
    query = select(User).where(User.email == email)
    if exclude_user_id is not None:
        query = query.where(User.id != exclude_user_id)
    existing = db.execute(query).scalars().first()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")


def ensure_assignee_exists(db: Session, user_id: Optional[int]) -> None:
    if user_id is None:
        return
    if db.get(User, user_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assigned user not found")


@app.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)) -> List[UserOut]:
    users = db.execute(select(User).order_by(User.id)).scalars().all()
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


@app.get("/tasks", response_model=List[TaskOut])
def list_tasks(db: Session = Depends(get_db)) -> List[TaskOut]:
    tasks = db.execute(select(OnboardingTask).order_by(OnboardingTask.id)).scalars().all()
    return [TaskOut.model_validate(task) for task in tasks]


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskOut:
    task = db.get(OnboardingTask, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskOut.model_validate(task)


@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> TaskOut:
    ensure_assignee_exists(db, payload.user_id)

    task = OnboardingTask(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskOut.model_validate(task)


@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)) -> TaskOut:
    task = db.get(OnboardingTask, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "user_id" in update_data:
        ensure_assignee_exists(db, update_data["user_id"])

    for field, value in update_data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return TaskOut.model_validate(task)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    task = db.get(OnboardingTask, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task)
    db.commit()


@app.get("/hr-dashboard", response_class=HTMLResponse)
def hr_dashboard_portal() -> HTMLResponse:
    """Serve an embedded frame that displays the Streamlit HR dashboard."""

    if not streamlit_enabled():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Streamlit UI is disabled. Set ENABLE_STREAMLIT_UI=1 to enable the dashboard.",
        )

    port = os.getenv("STREAMLIT_PORT", "8501")
    address = os.getenv("STREAMLIT_PUBLIC_ADDRESS", os.getenv("STREAMLIT_ADDRESS", "127.0.0.1"))
    iframe_url = f"http://{address}:{port}"
    html = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
        <head>
            <meta charset=\"utf-8\" />
            <title>OnboardPro HR Dashboard</title>
            <style>
                html, body {{ margin: 0; height: 100%; }}
                iframe {{ border: 0; width: 100%; height: 100%; }}
            </style>
        </head>
        <body>
            <iframe src=\"{iframe_url}\" title=\"OnboardPro HR Dashboard\"></iframe>
        </body>
    </html>
    """
    return HTMLResponse(content=html)
