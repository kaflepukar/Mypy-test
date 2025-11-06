from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models."""

    pass


class User(Base):
    """User Model - Core authentication and identity"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    # Relationships

    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User: {self.username}>"


class Project(Base):
    """Project Model - Stores portfolio projects with AI enhancement"""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # User's original input
    description: Mapped[str] = mapped_column(Text, nullable=False)
    highlights: Mapped[Optional[dict]] = mapped_column(JSON)  # Array of strings

    # AI-enhanced versions
    description_enhanced: Mapped[Optional[str]] = mapped_column(Text)
    highlights_enhanced: Mapped[Optional[dict]] = mapped_column(
        JSON
    )  # Array of strings

    # Enhancement tracking
    enhancement_prompt_used: Mapped[Optional[str]] = mapped_column(Text)
    last_enhanced_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    project_url: Mapped[Optional[str]] = mapped_column(String(500))
    github_url: Mapped[Optional[str]] = mapped_column(String(500))
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    technologies_used: Mapped[Optional[dict]] = mapped_column(JSON)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="projects")

    def __repr__(self):
        return f"<Project: {self.project_name}>"
