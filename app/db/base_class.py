from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models
    """

    id: Mapped[int]  # noqa: VNE003
