import uuid
from datetime import datetime

from sqlalchemy import DateTime, MetaData, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.utils.sqlalchemy.funcs import utcnow

POSTGRES_NAMING_CONVENTION = {
    "ix": "%(table_name)s_%(column_0_N_name)s_idx",
    "uq": "%(table_name)s_%(column_0_N_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models
    """

    __tablename__: str

    metadata = MetaData(naming_convention=POSTGRES_NAMING_CONVENTION)

    id: Mapped[uuid.UUID] = mapped_column(  # noqa: VNE003
        Uuid(as_uuid=True),
        primary_key=True,
        unique=True,  # only needs for alembic unique index
        index=True,
        default=uuid.uuid4,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=utcnow(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
    )
