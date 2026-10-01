"""團隊成員名稱改為只顯示暱稱

Revision ID: 0010
Revises: 0009
Create Date: 2026-10-01
"""
from alembic import op
import sqlalchemy as sa


revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None

# (舊名稱關鍵字, 舊名稱, 新名稱)
RENAMES = [
    ("家臻", "家臻 Emily", "Emily"),
    ("佩純", "佩純 Penny", "Penny"),
    ("偉鈞", "偉鈞 Leo", "九九"),
    ("佩彤", "佩彤 Wendy", "Wendy"),
]

team_members = sa.table("team_members", sa.column("name", sa.String))


def upgrade():
    for keyword, _, new_name in RENAMES:
        op.execute(
            team_members.update()
            .where(team_members.c.name.like(f"%{keyword}%"))
            .values(name=new_name)
        )


def downgrade():
    for _, old_name, new_name in RENAMES:
        op.execute(
            team_members.update()
            .where(team_members.c.name == new_name)
            .values(name=old_name)
        )
