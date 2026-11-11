from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func
)

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class ModelVersion(Base):

    __tablename__ = "model_versions"

    __table_args__ = (
        UniqueConstraint(
            "model_id",
            "version",
            name="uq_model_version"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    model_id: Mapped[int] = mapped_column(
        ForeignKey("monitored_models.id"),
        nullable=False
    )

    version: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    artifact_uri: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="registered",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )