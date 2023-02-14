from typing import Any

from pydantic import BaseModel


class Entity(BaseModel):
    """
    Generic entity schema.
    """

    id: Any

    @property
    def row_id(self) -> Any:
        """
        To avoid using a reserved Python name "id" use row_id instead.
        """
        if hasattr(self, "id") and self.id is not None:
            return self.id

        raise AttributeError(f'Entity {self.__repr_name__()} has no attribute "id"')

    class Config:
        orm_mode = True
