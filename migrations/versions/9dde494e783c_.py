"""empty message

Revision ID: 9dde494e783c
Revises: faffbff1c488
Create Date: 2021-05-14 00:15:48.349996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dde494e783c'
down_revision = 'faffbff1c488'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('customer', sa.Column('email_confirmed', sa.Boolean(),nullable=False, default=False))
    op.add_column('delivery_time_slot', sa.Column('status', sa.Boolean(), default=True))
    op.create_index(op.f('ix_delivery_time_slot_id'), 'delivery_time_slot', ['id'], unique=False)
    op.add_column('orders', sa.Column('delivery_street', sa.String(length=100), nullable=True))
    op.alter_column('orders', 'delivery_timeslot',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'orders', 'delivery_time_slot', ['delivery_timeslot'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.alter_column('orders', 'status',
               existing_type=sa.VARCHAR(length=40),
               nullable=False)
    op.alter_column('orders', 'delivery_timeslot',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('orders', 'delivery_street')
    op.drop_index(op.f('ix_delivery_time_slot_id'), table_name='delivery_time_slot')
    op.drop_column('delivery_time_slot', 'status')
    # ### end Alembic commands ###
