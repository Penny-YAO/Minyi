"""部署時自動更新資料庫結構。使用方式： python migrate_db.py

- 全新資料庫：依序執行所有 migration 建立資料表
- 導入 migration 前就存在的舊資料庫（有資料表但沒有 alembic_version）：
  先標記為初始版本 0001，再往後升級，不會重建或清空既有資料
"""
from flask_migrate import stamp, upgrade
from sqlalchemy import inspect

from app import create_app, db

app = create_app()

with app.app_context():
    tables = inspect(db.engine).get_table_names()
    if "alembic_version" not in tables and "works" in tables:
        print("偵測到既有資料庫，標記為初始版本 0001")
        stamp(revision="0001")
    upgrade()
    print("資料庫已更新至最新版本")
