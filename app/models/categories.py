from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.types import Type


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    type_id_default: Mapped[int | None] = mapped_column(
        ForeignKey("types.id", ondelete="SET NULL"), nullable=True
    )
    color: Mapped[str | None] = mapped_column(Text)
    icon_path: Mapped[str | None] = mapped_column(Text)
    icon_char: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
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

    type_default: Mapped[Type | None] = relationship(
        backref="categories_default", lazy="joined"
    )
