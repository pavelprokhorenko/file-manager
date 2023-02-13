from typing import Any, TypeVar

from sqlalchemy import Row, delete, insert, select, update

from src.db.base_class import Base
from src.db.session import async_postgres
from src.domain.common import BaseDTO
from src.domain.common.exceptions import RowNotFound
from src.domain.common.interfaces import AsyncDBRepositoryInterface

Model = TypeVar("Model", bound=Base)


class AsyncSQLAlchemyRepository(AsyncDBRepositoryInterface):
    """
    Asynchronous SQLAlchemy repository implementation.
    """

    def __init__(self, model: Model) -> None:
        self._model = model
        self._session = async_postgres.session

    async def receive(self, *, row_id: Any) -> Row:
        async with self._session() as session:
            query = select(self._model).where(self._model.id == row_id)
            scalar_result = await session.scalars(query)

            row = scalar_result.first()
            await session.commit()

        if not row:
            raise RowNotFound(
                f'Row with id "{row_id}" not found in table'
                f' "{self._model.__tablename__}"'
            )

        return row

    async def bulk_receive(self) -> list[Row]:
        async with self._session() as session:
            query = select(self._model)
            scalar_result = await session.scalars(query)

            rows = scalar_result.all()
            await session.commit()

        return rows

    async def create(self, dto: BaseDTO) -> Row:
        async with self._session() as session:
            query = (
                insert(self._model)
                .values(**dto.dict(exclude_unset=True))
                .returning(self._model)
            )
            scalar_result = await session.scalars(query)

            row = scalar_result.one()
            await session.commit()

        return row

    async def bulk_create(self, dtos: list[BaseDTO]) -> list[Row]:
        async with self._session() as session:
            new_rows_data = [dto.dict(exclude_unset=True) for dto in dtos]
            query = insert(self._model).values(new_rows_data).returning(self._model)
            scalar_result = await session.scalars(query)

            rows = scalar_result.all()
            await session.commit()

        return rows

    async def update(self, row_id: Any, dto: BaseDTO) -> Row:
        async with self._session() as session:
            query = (
                update(self._model)
                .values(**dto.dict(exclude_unset=True))
                .where(self._model.id == row_id)
                .returning(self._model)
            )
            scalar_result = await session.scalars(query)

            row = scalar_result.first()
            await session.commit()

        if not row:
            raise RowNotFound(
                f'Row with id "{row_id}" not found in table'
                f' "{self._model.__tablename__}"'
            )

        return row

    async def bulk_update(self, row_ids: Any, dto: BaseDTO) -> list[Row]:
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

    async def delete(self, row_id: Any) -> None:
        async with self._session() as session:
            query = delete(self._model).where(self._model.id == row_id)

            await session.execute(query)
            await session.commit()

    async def bulk_delete(self, row_ids: list[Any]) -> None:
        async with self._session() as session:
            query = delete(self._model).where(self._model.id.in_(row_ids))

            await session.execute(query)
            await session.commit()
