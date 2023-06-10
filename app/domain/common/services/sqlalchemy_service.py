from typing import Any, Generic

from app.domain.common.exceptions import SQLAlchemyServiceException
from app.domain.common.interfaces import AsyncDBServiceInterface
from app.domain.common.repositories import AsyncSQLAlchemyRepository
from app.domain.common.typevars import CreateDTO, Entity, Model, UpdateDTO


class AsyncSQLAlchemyService(AsyncDBServiceInterface, Generic[Entity, CreateDTO, UpdateDTO]):
    """
    Asynchronous SQLAlchemy service implementation.
    """

    def __init__(
        self,
        model: Model,
        entity: Entity,
        *,
        repository: type[AsyncSQLAlchemyRepository] = AsyncSQLAlchemyRepository,
    ) -> None:
        self._entity = entity
        self._repository = repository(model)

    async def receive(self, *, row_id: Any) -> Entity:
        row = await self._repository.receive(row_id=row_id)
        entity = self._entity.from_orm(row)
        return entity

    async def bulk_receive(self) -> list[Entity]:
        rows = await self._repository.bulk_receive()
        entities = [self._entity.from_orm(row) for row in rows]
        return entities

    async def create(self, dto: CreateDTO) -> Entity:
        entities_array = await self.bulk_create(dtos=[dto])
        return entities_array[0]

    async def bulk_create(self, dtos: list[CreateDTO]) -> list[Entity]:
        rows = await self._repository.bulk_create(dtos=dtos)
        entities = [self._entity.from_orm(row) for row in rows]
        return entities

    async def update(self, row_id: Any, dto: UpdateDTO) -> Entity:
        entities_array = await self.bulk_update(row_ids=[row_id], dto=dto)

        if not entities_array:
            raise SQLAlchemyServiceException(f'{self.__name__} cannot find object with id "{row_id}"')

        return entities_array[0]

    async def bulk_update(self, row_ids: Any, dto: UpdateDTO) -> list[Entity]:
        rows = await self._repository.bulk_update(row_ids=row_ids, dto=dto)
        entities = [self._entity.from_orm(row) for row in rows]
        return entities

    async def delete(self, row_id: Any) -> None:
        await self.bulk_delete(row_ids=[row_id])

    async def bulk_delete(self, row_ids: list[Any]) -> None:
        await self._repository.bulk_delete(row_ids=row_ids)
