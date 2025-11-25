from sqlalchemy import Date, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    date_start: Mapped[Date | None] = mapped_column(Date)
    date_end: Mapped[Date | None] = mapped_column(Date)

    description: Mapped[str | None] = mapped_column(Text)
    color: Mapped[str | None] = mapped_column(Text)

    date_created: Mapped[str] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
    date_modified: Mapped[str] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
