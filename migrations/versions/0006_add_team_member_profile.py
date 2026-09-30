"""team_members 新增 profile 欄位，並填入佩純的完整經歷

Revision ID: 0006
Revises: 0005
Create Date: 2026-09-30
"""
from alembic import op
import sqlalchemy as sa

from app.team_profiles import PENNY_PHOTO, PENNY_PROFILE


revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None

PLACEHOLDER_PHOTO = "/static/images/team/placeholder.jpg"


def upgrade():
    with op.batch_alter_table("team_members") as batch_op:
        batch_op.add_column(sa.Column("profile", sa.JSON(), nullable=True))

    team_members = sa.table(
        "team_members",
        sa.column("name", sa.String),
        sa.column("profile", sa.JSON),
        sa.column("photo_url", sa.String),
    )
    # 共用的示意照片改為空值，頁面改顯示「照片預留位置」，之後再換上各自的照片
    op.execute(
        team_members.update()
        .where(team_members.c.photo_url == PLACEHOLDER_PHOTO)
        .values(photo_url=None)
    )
    op.execute(
        team_members.update()
        .where(team_members.c.name.like("%佩純%"))
        .values(profile=PENNY_PROFILE, photo_url=PENNY_PHOTO)
    )


def downgrade():
    with op.batch_alter_table("team_members") as batch_op:
        batch_op.drop_column("profile")
