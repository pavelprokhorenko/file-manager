from typing import TypeVar

from app.db.base_class import Base
from app.domain.common.base_dto import BaseDTO
from app.domain.common.entity import Entity as BaseEntity

Entity = TypeVar("Entity", bound=BaseEntity)

Model = TypeVar("Model", bound=Base)

CreateDTO = TypeVar("CreateDTO", bound=BaseDTO)
UpdateDTO = TypeVar("UpdateDTO", bound=BaseDTO | None)
