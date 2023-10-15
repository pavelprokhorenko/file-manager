import uuid

from sqlalchemy import BigInteger, Boolean, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from src.db.base_class import Base


class FileSystemNodeMixin:
    """
    Mixin of file system objects (file and folder).
    """

    __table_args__ = (UniqueConstraint("name", "parent_folder_id"),)  # unique name of objects in the same folder

    name: Mapped[str] = mapped_column(String, nullable=False)

    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        server_default=expression.false(),
        nullable=False,
    )


class Folder(FileSystemNodeMixin, Base):
    __tablename__ = "folder"

    parent_folder_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey(
            "folder.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        comment='When "parent_folder_id" IS NULL, then this folder is root',
    )

    parent_folder: Mapped["Folder"] = relationship(back_populates="sub_folders", remote_side="Folder.id")

    sub_folders: Mapped[list["Folder"]] = relationship(
        back_populates="parent_folder",
    )

    files: Mapped[list["File"]] = relationship(
        back_populates="parent_folder",
    )


class File(FileSystemNodeMixin, Base):
    __tablename__ = "file"

    size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    parent_folder_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "folder.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    parent_folder: Mapped[Folder] = relationship(back_populates="files", remote_side="Folder.id")
