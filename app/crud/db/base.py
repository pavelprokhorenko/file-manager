from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base

Model = TypeVar("Model", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar(
    "UpdateSchemaType", bound=BaseModel | None
)  # sometimes update is not need


class CRUDBase(Generic[Model, CreateSchemaType, UpdateSchemaType]):
    """
    CRUD object with async default methods to Create, Read, Update, Delete (CRUD).
    """

    def __init__(self, model: type[Model]):
        self._model = model

    async def get_single(self, db: AsyncSession, *, model_id: int) -> Model | None:
        """Get single row by id."""
        obj = await self.get_multi(db, model_ids=[model_id])
        if obj:
            return obj[0]

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        model_ids: list[int],
        offset: int | None = None,
        limit: int | None = None
    ) -> list[Model]:
        """Get multiple rows."""
        async with db.begin():
            query = select(self._model).where(self._model.id.in_(model_ids))

            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)

            result = await db.execute(query)

        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_data: CreateSchemaType) -> Model:
        """Create row."""
        async with db.begin():
            query = (
                insert(self._model)
                .values(**obj_data.dict(exclude_unset=True))
                .returning(self._model)
            )
            result = await db.execute(query)

            await db.commit()
        return result.scalars().one()

    async def update(
        self,
        db: AsyncSession,
        *,
        model_id: int,
        updated_obj_data: UpdateSchemaType | dict[str, Any]
    ) -> Model:
        """Update row."""
        if isinstance(updated_obj_data, dict):
            updated_data = updated_obj_data
        else:
            updated_data = updated_obj_data.dict(exclude_unset=True)

        async with db.begin():
            query = (
                update(self._model)
                .values(**updated_data)
                .where(self._model.id == model_id)
                .returning(self._model)
            )
            result = await db.execute(query)

            await db.commit()
        return result.mappings().first()

    async def delete_multi(self, db: AsyncSession, *, model_ids: list[int]) -> None:
        """Delete multiple row."""
        async with db.begin():
            query = delete(self._model).where(self._model.id.in_(model_ids))
            await db.execute(query)
            await db.commit()

    async def delete_single(self, db: AsyncSession, *, model_id: int) -> None:
        """Delete single row."""
        await self.delete_multi(db, model_ids=[model_id])
