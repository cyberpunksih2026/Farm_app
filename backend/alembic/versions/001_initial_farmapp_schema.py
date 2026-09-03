"""001_initial_farmapp_schema

Revision ID: 001_initial_farmapp_schema
Revises: 
Create Date: 2026-09-02 16:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_farmapp_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('username', sa.String(length=50), nullable=False, unique=True),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=True, unique=True),
        sa.Column('phone', sa.String(length=30), nullable=True, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False, server_default='CUSTOMER'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('is_email_verified', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('email_verification_token', sa.String(length=255), nullable=True),
        sa.Column('password_reset_token', sa.String(length=255), nullable=True),
        sa.Column('password_reset_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('failed_login_attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('locked_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 2. farmers
    op.create_table(
        'farmers',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('farmer_code', sa.String(length=20), nullable=False, unique=True),
        sa.Column('name', sa.String(length=100), nullable=False, index=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('location', sa.String(length=100), nullable=False, index=True),
        sa.Column('state', sa.String(length=50), nullable=False, server_default='Tamil Nadu'),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('farm_size_acres', sa.Float(), nullable=True),
        sa.Column('verification_status', sa.String(length=20), nullable=False, server_default='VERIFIED'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 3. categories
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
        sa.Column('slug', sa.String(length=100), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 4. products
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('farmer_id', sa.Integer(), sa.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id', ondelete='RESTRICT'), nullable=False, index=True),
        sa.Column('name', sa.String(length=100), nullable=False, index=True),
        sa.Column('slug', sa.String(length=120), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('unit', sa.String(length=20), nullable=False, server_default='kg'),
        sa.Column('base_price', sa.Float(), nullable=False),
        sa.Column('farmer_price', sa.Float(), nullable=False),
        sa.Column('market_price', sa.Float(), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('is_organic', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('harvest_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 5. inventory
    op.create_table(
        'inventory',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('stock_quantity', sa.Float(), nullable=False, server_default='0'),
        sa.Column('reserved_quantity', sa.Float(), nullable=False, server_default='0'),
        sa.Column('min_threshold', sa.Float(), nullable=False, server_default='5.0'),
        sa.Column('unit', sa.String(length=20), nullable=False, server_default='kg'),
        sa.Column('last_restocked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 6. addresses
    op.create_table(
        'addresses',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('recipient_name', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('street', sa.String(length=255), nullable=False),
        sa.Column('landmark', sa.String(length=100), nullable=True),
        sa.Column('city', sa.String(length=50), nullable=False),
        sa.Column('state', sa.String(length=50), nullable=False, server_default='Tamil Nadu'),
        sa.Column('postal_code', sa.String(length=20), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 7. carts & cart_items
    op.create_table(
        'carts',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True, unique=True),
        sa.Column('session_id', sa.String(length=100), nullable=True, unique=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'cart_items',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('cart_id', sa.Integer(), sa.ForeignKey('carts.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('quantity', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('unit_price', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 8. orders & order_items
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('order_number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('delivery_address_id', sa.Integer(), sa.ForeignKey('addresses.id', ondelete='SET NULL'), nullable=True),
        sa.Column('subtotal', sa.Float(), nullable=False),
        sa.Column('delivery_fee', sa.Float(), nullable=False, server_default='0'),
        sa.Column('discount_amount', sa.Float(), nullable=False, server_default='0'),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='CREATED'),
        sa.Column('payment_status', sa.String(length=20), nullable=False, server_default='PENDING'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete='SET NULL'), nullable=True),
        sa.Column('farmer_id', sa.Integer(), sa.ForeignKey('farmers.id', ondelete='SET NULL'), nullable=True),
        sa.Column('product_name', sa.String(length=100), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False, server_default='kg'),
        sa.Column('unit_price', sa.Float(), nullable=False),
        sa.Column('farmer_price', sa.Float(), nullable=False),
        sa.Column('subtotal', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 9. payments
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('payment_method', sa.String(length=30), nullable=False, server_default='UPI'),
        sa.Column('payment_status', sa.String(length=30), nullable=False, server_default='PENDING'),
        sa.Column('transaction_id', sa.String(length=100), nullable=True, unique=True),
        sa.Column('gateway_response', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 10. deliveries
    op.create_table(
        'deliveries',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('tracking_number', sa.String(length=64), nullable=False, unique=True),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='PENDING'),
        sa.Column('current_lat', sa.Float(), nullable=True),
        sa.Column('current_lng', sa.Float(), nullable=True),
        sa.Column('estimated_delivery', sa.DateTime(timezone=True), nullable=True),
        sa.Column('actual_delivery', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 11. notifications
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('type', sa.String(length=30), nullable=False, server_default='SYSTEM'),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 12. ai_conversations & ai_messages
    op.create_table(
        'ai_conversations',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('conversation_id', sa.String(length=64), nullable=False, unique=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'ai_messages',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('conversation_id', sa.String(length=64), sa.ForeignKey('ai_conversations.conversation_id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tokens_used', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('ai_messages')
    op.drop_table('ai_conversations')
    op.drop_table('notifications')
    op.drop_table('deliveries')
    op.drop_table('payments')
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_table('cart_items')
    op.drop_table('carts')
    op.drop_table('addresses')
    op.drop_table('inventory')
    op.drop_table('products')
    op.drop_table('categories')
    op.drop_table('farmers')
    op.drop_table('users')
