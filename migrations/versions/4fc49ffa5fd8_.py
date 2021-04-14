"""empty message

Revision ID: 4fc49ffa5fd8
Revises: 
Create Date: 2021-04-13 23:20:49.367261

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4fc49ffa5fd8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('cart_ibfk_1', 'cart', type_='foreignkey')
    op.drop_constraint('cart_ibfk_2', 'cart', type_='foreignkey')
    op.create_foreign_key(None, 'cart', 'customer', ['cart_id'], ['id'])
    op.create_foreign_key(None, 'cart', 'grocery', ['item_id'], ['id'])
    op.alter_column('order', 'customer_id',
               existing_type=mysql.INTEGER())
    op.drop_constraint('order_ibfk_2', 'order', type_='foreignkey')
    op.drop_constraint('order_ibfk_1', 'order', type_='foreignkey')
    op.create_foreign_key(None, 'order', 'customer', ['customer_id'], ['id'])
    op.create_foreign_key(None, 'order', 'employee', ['checkout_by'], ['id'])
    op.drop_constraint('order_groceries_ibfk_2', 'order_groceries', type_='foreignkey')
    op.drop_constraint('order_groceries_ibfk_1', 'order_groceries', type_='foreignkey')
    op.create_foreign_key(None, 'order_groceries', 'order', ['order_id'], ['id'])
    op.create_foreign_key(None, 'order_groceries', 'grocery', ['grocery_id'], ['id'])
    op.drop_constraint('payment_ibfk_2', 'payment', type_='foreignkey')
    op.drop_constraint('payment_ibfk_1', 'payment', type_='foreignkey')
    op.create_foreign_key(None, 'payment', 'employee', ['recorded_by'], ['id'])
    op.create_foreign_key(None, 'payment', 'order', ['order_id'], ['id'])
    op.drop_constraint('rating_ibfk_2', 'rating', type_='foreignkey')
    op.drop_constraint('rating_ibfk_1', 'rating', type_='foreignkey')
    op.create_foreign_key(None, 'rating', 'grocery', ['item_id'], ['id'])
    op.create_foreign_key(None, 'rating', 'customer', ['cust_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rating', type_='foreignkey')
    op.drop_constraint(None, 'rating', type_='foreignkey')
    op.create_foreign_key('rating_ibfk_1', 'rating', 'customer', ['cust_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('rating_ibfk_2', 'rating', 'grocery', ['item_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'payment', type_='foreignkey')
    op.drop_constraint(None, 'payment', type_='foreignkey')
    op.create_foreign_key('payment_ibfk_1', 'payment', 'order', ['order_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('payment_ibfk_2', 'payment', 'employee', ['recorded_by'], ['id'], ondelete='SET NULL')
    op.drop_constraint(None, 'order_groceries', type_='foreignkey')
    op.drop_constraint(None, 'order_groceries', type_='foreignkey')
    op.create_foreign_key('order_groceries_ibfk_1', 'order_groceries', 'grocery', ['grocery_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('order_groceries_ibfk_2', 'order_groceries', 'order', ['order_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.create_foreign_key('order_ibfk_1', 'order', 'customer', ['customer_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('order_ibfk_2', 'order', 'employee', ['checkout_by'], ['id'], ondelete='SET NULL')
    op.alter_column('order', 'customer_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.create_foreign_key('cart_ibfk_2', 'cart', 'grocery', ['item_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('cart_ibfk_1', 'cart', 'customer', ['cart_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###