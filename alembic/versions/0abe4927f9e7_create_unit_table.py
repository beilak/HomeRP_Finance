"""create unit table

Revision ID: 0abe4927f9e7
Revises: e438d079fa50
Create Date: 2022-10-08 02:01:17.284113

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import PasswordType


# revision identifiers, used by Alembic.
revision = '0abe4927f9e7'
down_revision = 'e438d079fa50'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "unit",
        sa.Column("unit_id", sa.String(32), primary_key=True),
        sa.Column("description", sa.String(32)),
        sa.Column("admin", sa.String(32), sa.ForeignKey("user.login"), nullable=False),
        sa.Column("join_pass", PasswordType(schemes=['pbkdf2_sha512']), nullable=False),
        sa.Column("cr_date", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("upd_date", sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("unit")
