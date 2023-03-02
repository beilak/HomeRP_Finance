"""create unit_user table

Revision ID: 08c1d9fa2328
Revises: 0abe4927f9e7
Create Date: 2022-10-08 02:09:29.279881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08c1d9fa2328'
down_revision = '0abe4927f9e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "unit_user",
        sa.Column("unit_id", sa.String(32), sa.ForeignKey('unit.unit_id'), primary_key=True),
        sa.Column("login", sa.String(32), sa.ForeignKey('user.login'), primary_key=True),
        sa.Column("cr_date", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("upd_date", sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("unit_user")
