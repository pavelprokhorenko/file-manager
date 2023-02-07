import re
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate __tablename__ automatically. Convert `PascalCase` to `snake_case`.
        """
        obj_name = cls.__name__
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", obj_name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
