from abc import ABCMeta, abstractmethod
from typing import Any

from sqlalchemy import Row

from src.domain.common import BaseDTO


class AsyncDBRepositoryInterface(metaclass=ABCMeta):
    """
    Interface for CRUD database operations. Suited for SQL and NoSQL databases.
    Using async IO queries.
    """

    @abstractmethod
    async def receive(self, *, row_id: Any) -> Row:
        """
        Receive single row.
        """

    @abstractmethod
    async def bulk_receive(self) -> list[Row]:
        """
        Receive multiple rows.
        """

    @abstractmethod
    async def bulk_create(self, dtos: list[BaseDTO]) -> list[Row]:
        """
        Create new rows.
        """

    @abstractmethod
    async def bulk_update(self, row_ids: Any, dto: BaseDTO) -> list[Row]:
        """
        Update multiple rows with new data.
        """

    @abstractmethod
    async def bulk_delete(self, row_ids: list[Any]) -> None:
        """
        Delete multiple rows.
        """
