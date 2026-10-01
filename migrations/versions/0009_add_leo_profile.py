"""填入偉鈞的完整經歷

Revision ID: 0009
Revises: 0008
Create Date: 2026-10-01
"""
from alembic import op
import sqlalchemy as sa

from app.team_profiles import LEO_PROFILE


revision = "0009"
down_revision = "0008"
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
        .where(team_members.c.name.like("%偉鈞%"))
        .values(profile=LEO_PROFILE)
    )


def downgrade():
    team_members = sa.table(
        "team_members",
        sa.column("name", sa.String),
        sa.column("profile", sa.JSON(none_as_null=True)),
    )
    op.execute(
        team_members.update()
        .where(team_members.c.name.like("%偉鈞%"))
        .values(profile=None)
    )
