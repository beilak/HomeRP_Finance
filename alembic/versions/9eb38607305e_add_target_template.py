"""add target template

Revision ID: 9eb38607305e
Revises: c4ba5403c197
Create Date: 2023-07-08 23:26:39.924649

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '9eb38607305e'
down_revision = 'c4ba5403c197'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('target_cnt_template',
    sa.Column('template_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('value', sa.Numeric(precision=8), nullable=True),
    sa.Column('currency', sqlalchemy_utils.types.currency.CurrencyType(length=3), nullable=True),
    sa.PrimaryKeyConstraint('template_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('target_cnt_template')
    # ### end Alembic commands ###
