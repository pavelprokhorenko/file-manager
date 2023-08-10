class CoreException(Exception):
    """
    Base project exception
    """


class ServiceError(CoreException):
    """
    Error on service layer.
    """


class RowNotFound(ServiceError):
    """
    Row does not exists in database.
    """
