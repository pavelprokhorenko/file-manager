from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped

POSTGRES_NAMING_CONVENTION = {
    "ix": "%(table_name)s_%(column_0_name)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models
    """

    metadata = MetaData(naming_convention=POSTGRES_NAMING_CONVENTION)

    id: Mapped[int]  # noqa: VNE003
