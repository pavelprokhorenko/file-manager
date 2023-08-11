from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """
    Data Transfer Object for an arbitrary entity.
    """

    model_config = ConfigDict(
        frozen=True,
    )
