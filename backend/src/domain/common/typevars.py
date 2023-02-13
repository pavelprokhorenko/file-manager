from typing import TypeVar

from src.db.base_class import Base

Model = TypeVar("Model", bound=Base)
