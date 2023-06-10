import re

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    id: Mapped
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate __tablename__ automatically. Convert `PascalCase` to `snake_case`.
        """
        obj_name = cls.__name__
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", obj_name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
