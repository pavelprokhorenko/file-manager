from typing import Any

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):  # type: ignore[type-arg]
    """
    Implementation of current datetime in UTC timezone for different database dialects.
    """

    type = DateTime()  # noqa: VNE003
    inherit_cache = True


@compiles(utcnow, "postgresql")  # type: ignore[misc]
def postgres_utcnow(*args: Any, **kwargs: Any) -> str:
    """
    PostgreSQL impl of current datetime in UTC timezone.
    """
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
