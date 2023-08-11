import uuid
from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base_dto import BaseDTO
from src.db.base_class import Base

Model = TypeVar("Model", bound=Base)
CreateDTO = TypeVar("CreateDTO", bound=BaseDTO)
UpdateDTO = TypeVar("UpdateDTO", bound=BaseDTO)


class BaseService(Generic[Model, CreateDTO, UpdateDTO]):
    """
    Asynchronous SQLAlchemy service implementation.
    """

    _model: type[Model]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def receive(self, *, row_id: uuid.UUID) -> Model:
        query = select(self._model).where(self._model.id == row_id)
        scalar_result = await self._session.scalars(query)

        row = scalar_result.one()
        await self._session.commit()

        return row

    async def receive_for_update(self, *, row_id: uuid.UUID) -> Model:
        query = select(self._model).where(self._model.id == row_id).with_for_update()
        scalar_result = await self._session.scalars(query)

        row = scalar_result.one()
        await self._session.commit()

        return row

    async def bulk_receive(self) -> Sequence[Model]:
        query = select(self._model)
        scalar_result = await self._session.scalars(query)

        rows = scalar_result.all()
        await self._session.commit()

        return rows

    async def bulk_receive_for_update(self) -> Sequence[Model]:
        query = select(self._model).with_for_update()
        scalar_result = await self._session.scalars(query)

        rows = scalar_result.all()
        await self._session.commit()

        return rows

    async def bulk_create(self, dtos: list[CreateDTO]) -> Sequence[Model]:
        new_rows_data = [dto.dict(exclude_unset=True) for dto in dtos]
        query = insert(self._model).values(new_rows_data).returning(self._model)
        scalar_result = await self._session.scalars(query)

        rows = scalar_result.all()
        await self._session.commit()

        return rows

    async def bulk_update(self, row_ids: list[uuid.UUID], dto: UpdateDTO) -> Sequence[Model]:
        query = (
            update(self._model)
            .values(**dto.dict(exclude_unset=True))
            .where(self._model.id.in_(row_ids))
            .returning(self._model)
        )
        scalar_result = await self._session.scalars(query)

        rows = scalar_result.all()
        await self._session.commit()

        return rows

    async def bulk_delete(self, row_ids: list[uuid.UUID]) -> None:
        query = delete(self._model).where(self._model.id.in_(row_ids))

        await self._session.execute(query)
        await self._session.commit()
