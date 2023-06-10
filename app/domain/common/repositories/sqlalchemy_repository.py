from typing import Any

from sqlalchemy import Row, delete, insert, select, update

from app.db.session import async_postgres
from app.domain.common.exceptions import RowNotFound
from app.domain.common.interfaces import AsyncDBRepositoryInterface
from app.domain.common.typevars import CreateDTO, Model, UpdateDTO


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
            raise RowNotFound(f'Row with id "{row_id}" not found in table "{self._model.__tablename__}"')

        return row

    async def bulk_receive(self) -> list[Row]:
        async with self._session() as session:
            query = select(self._model)
            scalar_result = await session.scalars(query)

            rows = scalar_result.all()
            await session.commit()

        return rows

    async def bulk_create(self, dtos: list[CreateDTO]) -> list[Row]:
        async with self._session() as session:
            new_rows_data = [dto.dict(exclude_unset=True) for dto in dtos]
            query = insert(self._model).values(new_rows_data).returning(self._model)
            scalar_result = await session.scalars(query)

            rows = scalar_result.all()
            await session.commit()

        return rows

    async def bulk_update(self, row_ids: Any, dto: UpdateDTO) -> list[Row]:
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

    async def bulk_delete(self, row_ids: list[Any]) -> None:
        async with self._session() as session:
            query = delete(self._model).where(self._model.id.in_(row_ids))

            await session.execute(query)
            await session.commit()
