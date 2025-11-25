from sqlalchemy import DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Type(Base):
    __tablename__ = "types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    date_created: Mapped[str] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )

    date_modified: Mapped[str] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    notes: Mapped[str | None] = mapped_column(Text)
