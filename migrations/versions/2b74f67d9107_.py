"""empty message

Revision ID: 2b74f67d9107
Revises: 20236bba8a5d
Create Date: 2021-05-23 23:11:20.850670

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2b74f67d9107'
down_revision = '20236bba8a5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'card_payment', 'orders', ['order_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('cart_item_id_fkey', 'cart', type_='foreignkey')
    op.create_foreign_key(None, 'cart', 'grocery', ['item_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'cart', 'customer', ['cart_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'cash_payment', 'orders', ['order_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'cash_payment', 'employee', ['recorded_by'], ['id'], ondelete='SET NULL')
    op.create_index(op.f('ix_customer_id'), 'customer', ['id'], unique=False)
    op.create_unique_constraint(None, 'customer', ['email'])
    op.alter_column('delivery_parish', 'parish',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    op.create_unique_constraint(None, 'delivery_parish', ['parish'])
    op.add_column('employee', sa.Column('telephone', sa.LargeBinary(), nullable=True))
    op.create_index(op.f('ix_employee_id'), 'employee', ['id'], unique=False)
    op.create_unique_constraint(None, 'employee', ['email'])
    op.create_foreign_key(None, 'order_groceries', 'orders', ['order_id'], ['id'], ondelete='CASCADE')
    op.add_column('orders', sa.Column('delivery_parish', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)
    op.create_foreign_key(None, 'orders', 'customer', ['customer_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'orders', 'delivery_parish', ['delivery_parish'], ['id'])
    op.create_foreign_key(None, 'orders', 'delivery_time_slot', ['delivery_timeslot'], ['id'])
    op.create_foreign_key(None, 'orders', 'employee', ['checkout_by'], ['id'], ondelete='SET NULL')
    op.drop_constraint('rating_item_id_fkey', 'rating', type_='foreignkey')
    op.create_foreign_key(None, 'rating', 'customer', ['cust_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'rating', 'grocery', ['item_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('taxes_on_goods_tax_fkey', 'taxes_on_goods', type_='foreignkey')
    op.drop_constraint('taxes_on_goods_grocery_id_fkey', 'taxes_on_goods', type_='foreignkey')
    op.create_foreign_key(None, 'taxes_on_goods', 'taxes', ['tax'], ['tax'], ondelete='SET NULL')
    op.create_foreign_key(None, 'taxes_on_goods', 'grocery', ['grocery_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'taxes_on_goods', type_='foreignkey')
    op.drop_constraint(None, 'taxes_on_goods', type_='foreignkey')
    op.create_foreign_key('taxes_on_goods_grocery_id_fkey', 'taxes_on_goods', 'grocery', ['grocery_id'], ['id'])
    op.create_foreign_key('taxes_on_goods_tax_fkey', 'taxes_on_goods', 'taxes', ['tax'], ['tax'])
    op.drop_constraint(None, 'rating', type_='foreignkey')
    op.drop_constraint(None, 'rating', type_='foreignkey')
    op.create_foreign_key('rating_item_id_fkey', 'rating', 'grocery', ['item_id'], ['id'])
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_column('orders', 'delivery_parish')
    op.drop_constraint(None, 'order_groceries', type_='foreignkey')
    op.drop_constraint(None, 'employee', type_='unique')
    op.drop_index(op.f('ix_employee_id'), table_name='employee')
    op.drop_column('employee', 'telephone')
    op.drop_constraint(None, 'delivery_parish', type_='unique')
    op.alter_column('delivery_parish', 'parish',
               existing_type=postgresql.BYTEA(),
               nullable=False)
    op.drop_constraint(None, 'customer', type_='unique')
    op.drop_index(op.f('ix_customer_id'), table_name='customer')
    op.drop_constraint(None, 'cash_payment', type_='foreignkey')
    op.drop_constraint(None, 'cash_payment', type_='foreignkey')
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.create_foreign_key('cart_item_id_fkey', 'cart', 'grocery', ['item_id'], ['id'])
    op.drop_constraint(None, 'card_payment', type_='foreignkey')
    op.drop_table('total_quantity_purchased')
    op.drop_table('total_amount_purchased')
    op.drop_table('count_pairs')
    op.drop_table('item_total_rating')
    # ### end Alembic commands ###
