from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import FileVersion, Folder, User

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Boolean, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class File(Base):
    __tablename__ = "files"

    __table_args__ = (
        # prevent duplicate file names in same folder (only for active files)
        UniqueConstraint(
            "folder_id", "name", "is_deleted",
            name="uq_file_folder_name"
        ),

        # performance indexes
        Index("idx_file_folder", "folder_id"),
        Index("idx_file_owner", "owner_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    folder_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("folders.id"),
        nullable=False
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    # 🔗 relationships

    folder: Mapped["Folder"] = relationship(
        back_populates="files"
    )

    owner: Mapped["User"] = relationship(
        back_populates="files"
    )

    versions: Mapped[list["FileVersion"]] = relationship(
        back_populates="file",
        order_by="FileVersion.version_number"
    )