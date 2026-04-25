

import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    # Primary Key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # Unique Email
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    # Auth
    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    # Audit
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationship → folders
    folders: Mapped[list["Folder"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan"
    )