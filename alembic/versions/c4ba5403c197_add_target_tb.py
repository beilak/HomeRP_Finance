"""add target tb

Revision ID: c4ba5403c197
Revises: 
Create Date: 2023-03-02 23:09:51.491248

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'c4ba5403c197'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('target_cnt',
    sa.Column('target_cnt_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('unit_id', sa.String(length=32), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('value', sa.Numeric(precision=8), nullable=True),
    sa.Column('currency', sqlalchemy_utils.types.currency.CurrencyType(length=3), nullable=True),
    sa.Column('init_value', sa.Numeric(precision=8), nullable=True),
    sa.Column('init_currency', sqlalchemy_utils.types.currency.CurrencyType(length=3), nullable=True),
    sa.Column('user_login', sa.String(length=32), nullable=True),
    sa.Column('cr_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('upd_date', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('target_cnt_id')
    )
    op.create_table('target',
    sa.Column('target_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('target_cnt_id', sa.Integer(), nullable=True),
    sa.Column('user_login', sa.String(length=32), nullable=True),
    sa.Column('value', sa.Numeric(precision=8), nullable=True),
    sa.Column('currency', sqlalchemy_utils.types.currency.CurrencyType(length=3), nullable=True),
    sa.Column('cr_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('upd_date', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['target_cnt_id'], ['target_cnt.target_cnt_id'], ),
    sa.PrimaryKeyConstraint('target_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('target')
    op.drop_table('target_cnt')
    # ### end Alembic commands ###
