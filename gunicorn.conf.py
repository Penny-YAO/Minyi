"""gunicorn 會自動讀取此檔（不論 Render 的 Start Command 怎麼設定）。"""


def on_starting(server):
    # 在 master 啟動、worker 建立前執行一次，避免多個 worker 同時更新資料庫
    from migrate_db import run_migrations

    run_migrations()
