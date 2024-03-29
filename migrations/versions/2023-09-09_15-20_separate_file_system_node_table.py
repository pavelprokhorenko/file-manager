"""separate file_system_node table

Revision ID: 73367aa2e7d9
Revises: f6721c64a10f
Create Date: 2023-09-09 15:20:37.084708+00:00

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "73367aa2e7d9"
down_revision = "f6721c64a10f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "folder",
        sa.Column(
            "parent_folder_id",
            sa.Uuid(),
            nullable=True,
            comment='When "parent_folder_id" IS NULL, then this folder is root',
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("is_hidden", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["parent_folder_id"],
            ["folder.id"],
            name=op.f("folder_parent_folder_id_fkey"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("folder_pkey")),
        sa.UniqueConstraint("name", "parent_folder_id", name=op.f("folder_name_parent_folder_id_key")),
    )
    op.create_index(op.f("folder_id_idx"), "folder", ["id"], unique=True)
    op.create_table(
        "file",
        sa.Column("size", sa.BigInteger(), nullable=False),
        sa.Column("parent_folder_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("is_hidden", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["parent_folder_id"],
            ["folder.id"],
            name=op.f("file_parent_folder_id_fkey"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("file_pkey")),
        sa.UniqueConstraint("name", "parent_folder_id", name=op.f("file_name_parent_folder_id_key")),
    )
    op.create_index(op.f("file_id_idx"), "file", ["id"], unique=True)
    op.drop_index("file_system_node_id_idx", table_name="file_system_node")
    op.drop_table("file_system_node")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "file_system_node",
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("is_hidden", sa.BOOLEAN(), server_default=sa.text("true"), autoincrement=False, nullable=False),
        sa.Column(
            "is_folder",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=False,
            comment="Flag that shows that object is folder",
        ),
        sa.Column(
            "parent_folder_id",
            sa.UUID(),
            autoincrement=False,
            nullable=True,
            comment='When "parent_folder_id" IS NULL, then this object is root folder',
        ),
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("timezone('utc'::text, CURRENT_TIMESTAMP)"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("timezone('utc'::text, CURRENT_TIMESTAMP)"),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["parent_folder_id"],
            ["file_system_node.id"],
            name="file_system_node_parent_folder_id_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="file_system_node_pkey"),
        sa.UniqueConstraint("name", "is_folder", "parent_folder_id", name="file_system_node_name_key"),
    )
    op.create_index("file_system_node_id_idx", "file_system_node", ["id"], unique=False)
    op.drop_index(op.f("file_id_idx"), table_name="file")
    op.drop_table("file")
    op.drop_index(op.f("folder_id_idx"), table_name="folder")
    op.drop_table("folder")
    # ### end Alembic commands ###
