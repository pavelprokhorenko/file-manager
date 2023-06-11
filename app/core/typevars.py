from typing import TypeVar

from app.core.base_dto import BaseDTO
from app.core.entity import Entity as BaseEntity
from app.db.base_class import Base

Entity = TypeVar("Entity", bound=BaseEntity)

Model = TypeVar("Model", bound=Base)

CreateDTO = TypeVar("CreateDTO", bound=BaseDTO)
UpdateDTO = TypeVar("UpdateDTO", bound=BaseDTO)
