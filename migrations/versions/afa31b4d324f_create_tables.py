"""Create tables

Revision ID: afa31b4d324f
Revises:
Create Date: 2024-03-19 21:40:49.034207

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "afa31b4d324f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "breads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tipo", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "meats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tipo", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "optionals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tipo", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "status",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tipo", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "burgers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("bread_id", sa.Integer(), nullable=False),
        sa.Column("meat_id", sa.Integer(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["bread_id"],
            ["breads.id"],
        ),
        sa.ForeignKeyConstraint(
            ["meat_id"],
            ["meats.id"],
        ),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["status.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "burger_optional",
        sa.Column("burger_id", sa.Integer(), nullable=True),
        sa.Column("optional_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["burger_id"],
            ["burgers.id"],
        ),
        sa.ForeignKeyConstraint(
            ["optional_id"],
            ["optionals.id"],
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("burger_optional")
    op.drop_table("burgers")
    op.drop_table("status")
    op.drop_table("optionals")
    op.drop_table("meats")
    op.drop_table("breads")
    # ### end Alembic commands ###