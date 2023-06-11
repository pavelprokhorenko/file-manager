from app.infrastructure.exceptions import InfrastructureError


class RowNotFound(InfrastructureError):
    """
    Row does not exists in database.
    """
