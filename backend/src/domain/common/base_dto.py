from pydantic import BaseModel


class BaseDTO(BaseModel):
    """
    Data Transfer Object for an arbitrary entity.
    """

    class Meta:
        frozen = True
