import uuid
from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import delete, insert, select, update

from src.core.base_dto import BaseDTO
from src.core.exceptions import RowNotFound
from src.db.base_class import Base
from src.db.session import async_postgres

Model = TypeVar("Model", bound=Base)
CreateDTO = TypeVar("CreateDTO", bound=BaseDTO)
UpdateDTO = TypeVar("UpdateDTO", bound=BaseDTO)


class BaseService(Generic[Model, CreateDTO, UpdateDTO]):
    """
    Asynchronous SQLAlchemy service implementation.
    """

    def __init__(self, model: type[Model]) -> None:
        self._model = model
        self._session = async_postgres.session

    async def receive(self, *, row_id: uuid.UUID) -> Model:
        async with self._session() as session:
            query = select(self._model).where(self._model.id == row_id)
            scalar_result = await session.scalars(query)

            row = scalar_result.first()
            await session.commit()

        if not row:
            raise RowNotFound(
                f'Row with id "{row_id}" not found in table "{self._model.__tablename__}"',
            )

        return row

    async def bulk_receive(self) -> Sequence[Model]:
        async with self._session() as session:
            query = select(self._model)
            scalar_result = await session.scalars(query)

            rows = scalar_result.all()
            await session.commit()

        return rows

    async def bulk_create(self, dtos: list[CreateDTO]) -> Sequence[Model]:
        async with self._session() as session:
            new_rows_data = [dto.dict(exclude_unset=True) for dto in dtos]
            query = insert(self._model).values(new_rows_data).returning(self._model)
            scalar_result = await session.scalars(query)

            rows = scalar_result.all()
            await session.commit()

        return rows

    async def bulk_update(self, row_ids: list[uuid.UUID], dto: UpdateDTO) -> Sequence[Model]:
        async with self._session() as session:
            query = (
                update(self._model)
                .values(**dto.dict(exclude_unset=True))
                .where(self._model.id.in_(row_ids))
                .returning(self._model)
            )
            scalar_result = await session.scalars(query)

            rows = scalar_result.all()
            await session.commit()

        return rows

    async def bulk_delete(self, row_ids: list[uuid.UUID]) -> None:
        async with self._session() as session:
            query = delete(self._model).where(self._model.id.in_(row_ids))

            await session.execute(query)
            await session.commit()
