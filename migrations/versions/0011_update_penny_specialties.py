"""佩純的核心專長改為條列式、經歷補上工作說明，與其他成員的呈現方式一致

Revision ID: 0011
Revises: 0010
Create Date: 2026-10-01
"""
from alembic import op
import sqlalchemy as sa

from app.team_profiles import PENNY_PROFILE


revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade():
    team_members = sa.table(
        "team_members",
        sa.column("name", sa.String),
        sa.column("profile", sa.JSON),
    )
    op.execute(
        team_members.update()
        .where(team_members.c.name == "Penny")
        .values(profile=PENNY_PROFILE)
    )


def downgrade():
    # 舊版的敘述式內容已不在 team_profiles.py，無法還原
    pass
