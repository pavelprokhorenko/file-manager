from datetime import datetime

from pydantic import Field

from src.domain.common import BaseDTO


class _FileFolderDTO(BaseDTO):
    """
    Common fields for file and folder.
    """

    name: str
    is_hidden: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    parent_folder_id: int | None


class _FileFolderUpdateDTO(BaseDTO):
    """
    Common fields for file and folder.
    """

    name: str | None
    is_hidden: bool | None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    parent_folder_id: int | None


class FileSystemNodeDTO(_FileFolderDTO):
    """
    Data Transfer Object for FileSystemNode.
    """

    is_folder: bool


class FileSystemNodeUpdateDTO(_FileFolderUpdateDTO):
    """
    Data Transfer Object for update FileSystemNode.
    """
