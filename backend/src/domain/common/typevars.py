from typing import TypeVar

from src.db.base_class import Base
from src.domain.common.base_dto import BaseDTO
from src.domain.common.entity import Entity as BaseEntity

Entity = TypeVar("Entity", bound=BaseEntity)

Model = TypeVar("Model", bound=Base)

CreateDTO = TypeVar("CreateDTO", bound=BaseDTO)
UpdateDTO = TypeVar("UpdateDTO", bound=BaseDTO | None)
