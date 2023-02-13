from abc import ABCMeta, abstractmethod
from typing import Any

from src.domain.common import BaseDTO, Entity


class AsyncDBRepositoryInterface(metaclass=ABCMeta):
    """
    Interface for CRUD database operations. Suited for SQL and NoSQL databases.
    Using async IO queries.
    """

    @abstractmethod
    async def receive(self, *, row_id: Any) -> Entity:
        """
        Receive single row.
        """

    @abstractmethod
    async def bulk_receive(self) -> list[Entity]:
        """
        Receive multiple rows.
        """

    @abstractmethod
    async def create(self, dto: BaseDTO) -> Entity:
        """
        Create new row.
        """

    @abstractmethod
    async def bulk_create(self, dtos: list[BaseDTO]) -> list[Entity]:
        """
        Create new rows.
        """

    @abstractmethod
    async def update(self, row_id: Any, dto: BaseDTO) -> Entity:
        """
        Update existing row with new data.
        """

    @abstractmethod
    async def bulk_update(self, row_ids: Any, dto: BaseDTO) -> list[Entity]:
        """
        Update multiple rows with new data.
        """

    @abstractmethod
    async def delete(self, row_id: Any) -> None:
        """
        Delete single row.
        """

    @abstractmethod
    async def bulk_delete(self, row_ids: list[Any]) -> None:
        """
        Delete multiple rows.
        """
