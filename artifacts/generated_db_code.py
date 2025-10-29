from datetime import datetime
from sqlalchemy import (
    String, Integer, DateTime, ForeignKey, Boolean, Enum, Text, UniqueConstraint, CheckConstraint, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import enum


class Base(DeclarativeBase):
    pass


class UserRole(enum.Enum):
    Admin = "Admin"
    Hiring_Manager = "Hiring Manager"
    New_Hire = "New Hire"


class ProcessStatus(enum.Enum):
    Not_Started = "Not Started"
    In_Progress = "In Progress"
    Completed = "Completed"


class AssignedTaskStatus(enum.Enum):
    Pending = "Pending"
    Completed = "Completed"


class Company(Base):
    __tablename__ = "companies"

    company_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    users: Mapped[list["User"]] = relationship("User", back_populates="company", cascade="all, delete-orphan")
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="company", cascade="all, delete-orphan")
    onboarding_plans: Mapped[list["OnboardingPlan"]] = relationship("OnboardingPlan", back_populates="company", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="userrole"), nullable=False)
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    company: Mapped["Company"] = relationship("Company", back_populates="users")
    manager: Mapped["User | None"] = relationship(
        "User",
        remote_side=[user_id],
        back_populates="reports",
        passive_deletes=True
    )
    reports: Mapped[list["User"]] = relationship(
        "User",
        back_populates="manager",
        cascade="all, save-update"
    )
    uploaded_documents: Mapped[list["Document"]] = relationship(
        "Document",
        back_populates="uploaded_by_user",
        foreign_keys="[Document.uploaded_by_user_id]"
    )
    created_onboarding_plans: Mapped[list["OnboardingPlan"]] = relationship(
        "OnboardingPlan",
        back_populates="created_by_user",
        foreign_keys="[OnboardingPlan.created_by_user_id]"
    )
    onboarding_processes_as_new_hire: Mapped["OnboardingProcess | None"] = relationship(
        "OnboardingProcess",
        back_populates="new_hire_user",
        foreign_keys="[OnboardingProcess.new_hire_user_id]",
        uselist=False,
        cascade="all, delete-orphan"
    )
    onboarding_processes_as_hiring_manager: Mapped[list["OnboardingProcess"]] = relationship(
        "OnboardingProcess",
        back_populates="hiring_manager_user",
        foreign_keys="[OnboardingProcess.hiring_manager_user_id]"
    )
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    file_type: Mapped[str | None] = mapped_column(String, nullable=True)
    uploaded_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    company: Mapped["Company"] = relationship("Company", back_populates="documents")
    uploaded_by_user: Mapped["User | None"] = relationship("User", back_populates="uploaded_documents")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="document")


class OnboardingPlan(Base):
    __tablename__ = "onboarding_plans"
    __table_args__ = (
        UniqueConstraint("company_id", "title"),
    )

    plan_id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    company: Mapped["Company"] = relationship("Company", back_populates="onboarding_plans")
    created_by_user: Mapped["User | None"] = relationship("User", back_populates="created_onboarding_plans")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="plan", cascade="all, delete-orphan")
    onboarding_processes: Mapped[list["OnboardingProcess"]] = relationship(
        "OnboardingProcess",
        back_populates="plan"
    )


class Task(Base):
    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("onboarding_plans.plan_id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    due_days_after_start: Mapped[int] = mapped_column(Integer, nullable=False)
    order_in_plan: Mapped[int] = mapped_column(Integer, nullable=False)
    document_id: Mapped[int | None] = mapped_column(ForeignKey("documents.document_id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    plan: Mapped["OnboardingPlan"] = relationship("OnboardingPlan", back_populates="tasks")
    document: Mapped["Document | None"] = relationship("Document", back_populates="tasks")
    assigned_tasks: Mapped[list["AssignedTask"]] = relationship("AssignedTask", back_populates="task")


class OnboardingProcess(Base):
    __tablename__ = "onboarding_processes"
    __table_args__ = (
        UniqueConstraint("new_hire_user_id"),
    )

    process_id: Mapped[int] = mapped_column(primary_key=True)
    new_hire_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    plan_id: Mapped[int] = mapped_column(ForeignKey("onboarding_plans.plan_id", ondelete="RESTRICT"), nullable=False)
    hiring_manager_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[ProcessStatus] = mapped_column(Enum(ProcessStatus, name="processstatus"), nullable=False, default=ProcessStatus.Not_Started)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    new_hire_user: Mapped["User"] = relationship(
        "User",
        back_populates="onboarding_processes_as_new_hire",
        foreign_keys=[new_hire_user_id]
    )
    plan: Mapped["OnboardingPlan"] = relationship("OnboardingPlan", back_populates="onboarding_processes")
    hiring_manager_user: Mapped["User"] = relationship(
        "User",
        back_populates="onboarding_processes_as_hiring_manager",
        foreign_keys=[hiring_manager_user_id]
    )
    assigned_tasks: Mapped[list["AssignedTask"]] = relationship("AssignedTask", back_populates="process", cascade="all, delete-orphan")


class AssignedTask(Base):
    __tablename__ = "assigned_tasks"
    __table_args__ = (
        UniqueConstraint("process_id", "task_id"),
    )

    assigned_task_id: Mapped[int] = mapped_column(primary_key=True)
    process_id: Mapped[int] = mapped_column(ForeignKey("onboarding_processes.process_id", ondelete="CASCADE"), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.task_id", ondelete="RESTRICT"), nullable=False)
    status: Mapped[AssignedTaskStatus] = mapped_column(Enum(AssignedTaskStatus, name="assignedtaskstatus"), nullable=False, default=AssignedTaskStatus.Pending)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    process: Mapped["OnboardingProcess"] = relationship("OnboardingProcess", back_populates="assigned_tasks")
    task: Mapped["Task"] = relationship("Task", back_populates="assigned_tasks")


class Notification(Base):
    __tablename__ = "notifications"

    notification_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="notifications")



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from .models import Base  # Adjust import if models are in another location

DATABASE_URL = "sqlite:///artifacts/onboarding.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Auto-create tables for dev/local use
Base.metadata.create_all(bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()