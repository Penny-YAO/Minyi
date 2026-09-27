"""新增後台帳號資料表 admin_users

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-27
"""
import os
from datetime import datetime

from alembic import op
import sqlalchemy as sa


revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    admin_users = op.create_table(
        "admin_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )

    if op.get_bind().dialect.name == "postgresql":
        # Supabase 會透過 REST API 對外公開 public schema 的資料表，
        # 開啟 RLS 且不建立任何 policy，anon / authenticated 角色就讀不到密碼雜湊；
        # 網站本身以資料表擁有者連線，不受 RLS 影響
        op.execute("ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY")

    # 原本存在環境變數的帳密搬進資料表，部署後可用原帳密登入
    username = os.environ.get("ADMIN_USERNAME", "admin").strip()
    password_hash = os.environ.get("ADMIN_PASSWORD_HASH", "").strip()
    if username and password_hash:
        op.bulk_insert(
            admin_users,
            [{
                "username": username,
                "password_hash": password_hash,
                "is_active": True,
                "created_at": datetime.utcnow(),
            }],
        )


def downgrade():
    op.drop_table("admin_users")
