from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import File

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class FileVersion(Base):
    __tablename__ = "file_versions"

    __table_args__ = (
        # prevent duplicate version numbers per file
        UniqueConstraint("file_id", "version_number", name="uq_file_version"),
        # performance
        Index("idx_file_version_file", "file_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("files.id"), nullable=False
    )

    storage_key: Mapped[str] = mapped_column(String(512), nullable=False)

    size: Mapped[int] = mapped_column(Integer, nullable=False)

    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)

    version_number: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # 🔗 relationship
    file: Mapped["File"] = relationship(back_populates="versions")
