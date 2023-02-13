from typing import TypeVar

from src.db.base_class import Base
from src.domain.common.base_dto import BaseDTO

Model = TypeVar("Model", bound=Base)

CreateDTO = TypeVar("CreateDTO", bound=BaseDTO)
UpdateDTO = TypeVar("UpdateDTO", bound=BaseDTO | None)
