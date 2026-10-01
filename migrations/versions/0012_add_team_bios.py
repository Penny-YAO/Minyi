"""填入成員卡片上的簡短說明（bio）

Revision ID: 0012
Revises: 0011
Create Date: 2026-10-01
"""
from alembic import op
import sqlalchemy as sa

from app.team_profiles import TEAM_BIOS


revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None

team_members = sa.table(
    "team_members",
    sa.column("name", sa.String),
    sa.column("bio", sa.Text),
)


def upgrade():
    for name, bio in TEAM_BIOS.items():
        op.execute(
            team_members.update()
            .where(team_members.c.name == name)
            .values(bio=bio)
        )


def downgrade():
    op.execute(
        team_members.update()
        .where(team_members.c.name.in_(list(TEAM_BIOS)))
        .values(bio=None)
    )
