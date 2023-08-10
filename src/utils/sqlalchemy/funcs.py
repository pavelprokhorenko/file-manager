from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):
    """
    Implementation of current datetime in UTC timezone for different database dialects.
    """

    type = DateTime()  # noqa: VNE003
    inherit_cache = True


@compiles(utcnow, "postgresql")
def postgres_utcnow(*args, **kwargs) -> str:
    """
    PostgreSQL impl of current datetime in UTC timezone.
    """
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
