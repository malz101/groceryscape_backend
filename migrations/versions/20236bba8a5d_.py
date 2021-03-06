"""empty message

Revision ID: 20236bba8a5d
Revises: e839960818a7
Create Date: 2021-05-19 18:47:39.281235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20236bba8a5d'
down_revision = 'e839960818a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('item_total_rating',
    # sa.Column('item_id', sa.Integer(), nullable=False),
    # sa.Column('total_rating', sa.Integer(), nullable=True),
    # sa.Column('num_customer', sa.Integer(), nullable=True),
    # sa.Column('coefficient', sa.Numeric(precision=15, scale=10), nullable=True),
    # sa.PrimaryKeyConstraint('item_id')
    # )
    # op.create_table('count_pairs',
    # sa.Column('item1', sa.Integer(), nullable=False),
    # sa.Column('item2', sa.Integer(), nullable=False),
    # sa.Column('count', sa.Integer(), nullable=True),
    # sa.ForeignKeyConstraint(['item1'], ['grocery.id'], ),
    # sa.ForeignKeyConstraint(['item2'], ['grocery.id'], ),
    # sa.PrimaryKeyConstraint('item1', 'item2')
    # )
    op.create_table('delivery_parish_',
    sa.Column('parish', sa.LargeBinary(),primary_key=True, nullable=False),
    sa.Column('delivery_rate', sa.Numeric(10,2), nullable=False)
    )

    op.create_table('orders_',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('orderdate', sa.DateTime(), nullable=False),
    sa.Column('status', sa.LargeBinary(), nullable=True),
    sa.Column('delivery_timeslot', sa.Integer(), nullable=True),
    sa.Column('payment_type', sa.LargeBinary(), nullable=True),
    sa.Column('delivery_date', sa.Date(), nullable=True),
    sa.Column('delivery_street', sa.LargeBinary(), nullable=True),
    sa.Column('delivery_town', sa.LargeBinary(), nullable=True),
    sa.Column('delivery_parish', sa.LargeBinary(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('checkout_by', sa.Integer(), nullable=True),
    sa.Column('details', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['checkout_by'], ['employees.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['delivery_parish'], ['delivery_parish_.parish'], ),
    sa.ForeignKeyConstraint(['delivery_timeslot'], ['delivery_time_slot.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders__id'), 'orders_', ['id'], unique=False)
    # op.create_table('total_amount_purchased',
    # sa.Column('cust_id', sa.Integer(), nullable=False),
    # sa.Column('grocery_id', sa.Integer(), nullable=False),
    # sa.Column('total', sa.Integer(), nullable=True),
    # sa.ForeignKeyConstraint(['cust_id'], ['customer.id'], ),
    # sa.ForeignKeyConstraint(['grocery_id'], ['grocery.id'], ),
    # sa.PrimaryKeyConstraint('cust_id', 'grocery_id')
    # )
    # op.create_table('total_quantity_purchased',
    # sa.Column('grocery_id', sa.Integer(), nullable=False),
    # sa.Column('total', sa.Integer(), nullable=True),
    # sa.ForeignKeyConstraint(['grocery_id'], ['grocery.id'], ),
    # sa.PrimaryKeyConstraint('grocery_id')
    # )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('total_quantity_purchased')
    # op.drop_table('total_amount_purchased')
    op.drop_index(op.f('ix_orders__id'), table_name='orders_')
    op.drop_table('orders_')
    # op.drop_table('count_pairs')
    # op.drop_table('item_total_rating')
    # ### end Alembic commands ###
