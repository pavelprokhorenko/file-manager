from typing import Any

from pydantic import BaseModel


class Entity(BaseModel):
    """
    Generic entity schema.
    """

    @property
    def row_id(self) -> Any:
        """
        To avoid using a reserved Python name "id" use row_id instead.
        """
        if id_ := getattr(self, "id", None):
            return id_

        raise AttributeError('Entity has no attribute "id"')

    class Config:
        orm_mode = True
