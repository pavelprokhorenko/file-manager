from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import expression, func

from app.db.base import Base


class FileSystemNode(Base):
    """
    Implementation of file system objects (file and folder).
    """

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    is_hidden = Column(Boolean, server_default=expression.true(), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.utcnow(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.utcnow(),
        server_onupdate=func.utcnow(),
        nullable=False,
    )
    is_folder = Column(Boolean, server_default=expression.false(), nullable=False)

    parent_folder_id = Column(
        Integer,
        ForeignKey("file_system_node.id", ondelete="CASCADE", onupdate="CASCADE"),
        comment='When "parent_folder_id" IS NULL, then this object is root folder',
    )
