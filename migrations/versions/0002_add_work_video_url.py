"""works 新增 video_url 欄位

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-26
"""
from alembic import op
import sqlalchemy as sa


revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    # 舊資料庫可能已手動加過此欄位（ALTER TABLE），存在就略過
    columns = [c["name"] for c in sa.inspect(op.get_bind()).get_columns("works")]
    if "video_url" not in columns:
        with op.batch_alter_table("works") as batch_op:
            batch_op.add_column(sa.Column("video_url", sa.String(length=255), nullable=True))


def downgrade():
    with op.batch_alter_table("works") as batch_op:
        batch_op.drop_column("video_url")
