"""changed order.details to order.notes

Revision ID: d7c62ac18295
Revises: 2b74f67d9107
Create Date: 2021-05-24 01:14:57.978412

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd7c62ac18295'
down_revision = '2b74f67d9107'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('notes', sa.LargeBinary(), nullable=True))
    op.drop_column('orders', 'details')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('details', postgresql.BYTEA(), autoincrement=False, nullable=True))
    op.drop_column('orders', 'notes')
    # ### end Alembic commands ###
