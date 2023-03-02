"""create user table

Revision ID: e438d079fa50
Revises: 
Create Date: 2022-10-08 01:32:11.141676

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import PasswordType, EmailType

# revision identifiers, used by Alembic.
revision = 'e438d079fa50'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("login", sa.String(32), primary_key=True),
        sa.Column("password", PasswordType(schemes=['pbkdf2_sha512']), nullable=False),
        sa.Column("first_name", sa.String(32)),
        sa.Column("last_name", sa.String(32)),
        sa.Column("email", EmailType),
        sa.Column("cr_date", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("upd_date", sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("user")
