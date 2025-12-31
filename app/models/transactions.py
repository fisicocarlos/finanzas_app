from sqlalchemy import Date, DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.categories import Category
from app.models.trips import Trip
from app.models.types import Type


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    date: Mapped[Date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    type_id: Mapped[int | None] = mapped_column(
        ForeignKey("types.id", ondelete="NO ACTION"), nullable=True
    )
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    trip_id: Mapped[int | None] = mapped_column(
        ForeignKey("trips.id", ondelete="SET NULL"), nullable=True
    )

    notes: Mapped[str | None] = mapped_column(Text)

    date_created: Mapped[str] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
    date_modified: Mapped[str] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    type: Mapped[Type | None] = relationship(lazy="joined")
    category: Mapped[Category | None] = relationship(lazy="joined")
    trip: Mapped[Trip | None] = relationship(lazy="joined")
