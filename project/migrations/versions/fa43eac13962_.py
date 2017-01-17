"""empty message

Revision ID: fa43eac13962
Revises: 91a69ccbcb90
Create Date: 2017-01-16 23:52:53.802802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa43eac13962'
down_revision = '91a69ccbcb90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reminder', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'reminder', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reminder', type_='foreignkey')
    op.drop_column('reminder', 'user_id')
    # ### end Alembic commands ###