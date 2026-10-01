"""填入 Wendy 的完整經歷

Revision ID: 0013
Revises: 0012
Create Date: 2026-10-01
"""
from alembic import op
import sqlalchemy as sa

from app.team_profiles import WENDY_PROFILE


revision = "0013"
down_revision = "0012"
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
        .where(team_members.c.name == "Wendy")
        .values(profile=WENDY_PROFILE)
    )


def downgrade():
    team_members = sa.table(
        "team_members",
        sa.column("name", sa.String),
        sa.column("profile", sa.JSON(none_as_null=True)),
    )
    op.execute(
        team_members.update()
        .where(team_members.c.name == "Wendy")
        .values(profile=None)
    )
