from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.db.base_class import Base
from app.models.sqlalchemy.funcs import utcnow


class FileSystemNode(Base):
    """
    Implementation of file system objects (file and folder).

    FileSystemNode means both file and folder, because they are actually the same thing in the system
    with one difference: file data is stored in AWS storage.
    But for database is the same thing, so they are merged into 1 table.

    For instance, there might be such a structure:

    ├── FileSystemNode(id=1, name="root folder", is_folder=True, ...)
    │    ├── FileSystemNode(id=5, name="scan.pdf", is_folder=False, parent_folder_id=1, ...)
    │    ├── FileSystemNode(id=6, name="schedule of lessons.xlsx", is_folder=False, parent_folder_id=1, ...)
    │    └── FileSystemNode(id=2, name="important", is_folder=True, parent_folder_id=1, ...)
    │    │   ├── FileSystemNode(id=3, name="cat.png", is_folder=False, parent_folder_id=2, ...)
    │    │   ├── FileSystemNode(id=4, name="document.docx", is_folder=False, parent_folder_id=2, ...)
    │    │   └── FileSystemNode(id=7, name="very important!", is_folder=True, parent_folder_id=2, ...)
    │    │       └── ...
    │    └── FileSystemNode(id=8, name="films", is_folder=True, parent_folder_id=1, ...)
    │        └── ...
    """

    __table_args__ = (
        UniqueConstraint("name", "is_folder", "parent_folder_id"),  # unique name of objects in the same folder
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # noqa: VNE003
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, server_default=expression.true(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=utcnow(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=utcnow(), nullable=False)
    is_folder: Mapped[bool] = mapped_column(
        Boolean,
        server_default=expression.false(),
        nullable=False,
        comment="Flag that shows that object is folder",
    )

    parent_folder_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("file_system_node.id", ondelete="CASCADE", onupdate="CASCADE"),
        comment='When "parent_folder_id" IS NULL, then this object is root folder',
    )
