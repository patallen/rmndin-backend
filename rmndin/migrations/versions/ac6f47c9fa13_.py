"""empty message

Revision ID: ac6f47c9fa13
Revises: d08bb1db0e09
Create Date: 2017-01-19 03:31:39.945808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac6f47c9fa13'
down_revision = 'd08bb1db0e09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reminder', sa.Column('fulfilled', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reminder', 'fulfilled')
    # ### end Alembic commands ###