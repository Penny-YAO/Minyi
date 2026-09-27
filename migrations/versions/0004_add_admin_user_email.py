"""admin_users 新增 email 欄位

Revision ID: 0004
Revises: 0003
Create Date: 2026-09-27
"""
from alembic import op
import sqlalchemy as sa


revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    # 既有帳號沒有信箱，欄位允許空值
    with op.batch_alter_table("admin_users") as batch_op:
        batch_op.add_column(sa.Column("email", sa.String(length=120), nullable=True))


def downgrade():
    with op.batch_alter_table("admin_users") as batch_op:
        batch_op.drop_column("email")
