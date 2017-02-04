"""Add verified column to user

Revision ID: 29b0a49bfa22
Revises: 867c0953fb7c
Create Date: 2017-02-04 03:47:15.649949

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '29b0a49bfa22'
down_revision = '867c0953fb7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reminder', 'type_')
    op.drop_column('reminder', 'delivery_method')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reminder', sa.Column('delivery_method', postgresql.ENUM(u'email', u'reddit', name='delivery_method_enum'), autoincrement=False, nullable=False))
    op.add_column('reminder', sa.Column('type_', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
