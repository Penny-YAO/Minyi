import click
from flask import Blueprint

from app import db
from app.models import AdminUser

admin_cli = Blueprint("admin_cli", __name__, cli_group=None)


@admin_cli.cli.command("set-admin")
@click.argument("username")
@click.password_option("--password", prompt="密碼", confirmation_prompt="再次輸入密碼")
def set_admin(username, password):
    """新增後台帳號，或重設既有帳號的密碼（並重新啟用）。"""
    user = AdminUser.query.filter_by(username=username).first()
    created = user is None
    if created:
        user = AdminUser(username=username)
        db.session.add(user)

    user.set_password(password)
    user.is_active = True
    db.session.commit()

    click.echo(f"後台帳號 {username} {'已新增' if created else '密碼已更新'}")
