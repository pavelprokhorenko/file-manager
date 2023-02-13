from abc import ABCMeta, abstractmethod
from typing import Any

from src.domain.common import BaseDTO, Entity

from .async_db_repository_interface import AsyncDBRepositoryInterface


class AsyncDBServiceInterface(metaclass=ABCMeta):
    """
    High level interface for CRUD operations that sends to database repository.
    """

    _repository: AsyncDBRepositoryInterface

    @abstractmethod
    async def receive(self, *, row_id: Any) -> Entity:
        """
        Receive single entity.
        """

    @abstractmethod
    async def bulk_receive(self) -> list[Entity]:
        """
        Receive multiple entity.
        """

    @abstractmethod
    async def create(self, dto: BaseDTO) -> Entity:
        """
        Create new entity.
        """

    @abstractmethod
    async def bulk_create(self, dtos: list[BaseDTO]) -> list[Entity]:
        """
        Create new entities.
        """

    @abstractmethod
    async def update(self, row_id: Any, dto: BaseDTO) -> Entity:
        """
        Update existing entity with new data.
        """

    @abstractmethod
    async def bulk_update(self, row_ids: Any, dto: BaseDTO) -> list[Entity]:
        """
        Update multiple entities with new data.
        """

    @abstractmethod
    async def delete(self, row_id: Any) -> None:
        """
        Delete single entity.
        """

    @abstractmethod
    async def bulk_delete(self, row_ids: list[Any]) -> None:
        """
        Delete multiple entities.
        """
