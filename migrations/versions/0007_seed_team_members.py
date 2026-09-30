"""team_members 為空時建立四位團隊成員

正式機從未執行 seed.py，team_members 沒有資料，0006 找不到佩純可更新。
已有成員資料的資料庫不做任何變更。

Revision ID: 0007
Revises: 0006
Create Date: 2026-09-30
"""
from alembic import op
import sqlalchemy as sa

from app.team_profiles import PENNY_PHOTO, PENNY_PROFILE


revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade():
    team_members = sa.table(
        "team_members",
        sa.column("name", sa.String),
        sa.column("role", sa.String),
        sa.column("photo_url", sa.String),
        sa.column("profile", sa.JSON(none_as_null=True)),
        sa.column("order", sa.Integer),
    )
    count = op.get_bind().execute(sa.select(sa.func.count()).select_from(team_members)).scalar()
    if count:
        return

    op.bulk_insert(team_members, [
        {"name": "家臻 Emily", "role": "美編", "photo_url": None, "profile": None, "order": 1},
        {"name": "佩純 Penny", "role": "系統分析規劃", "photo_url": PENNY_PHOTO, "profile": PENNY_PROFILE, "order": 2},
        {"name": "偉鈞 Leo", "role": "全端工程師 / 資料庫分析", "photo_url": None, "profile": None, "order": 3},
        {"name": "佩彤 Wendy", "role": "全端工程師 / 資料庫分析", "photo_url": None, "profile": None, "order": 4},
    ])


def downgrade():
    # 無法分辨成員是否由此 migration 建立，不刪除資料
    pass
