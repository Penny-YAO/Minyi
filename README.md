# Minyi Studio

個人工作室官方網站，使用 Python + Flask 建構，內容涵蓋核心理念、團隊成員介紹、案例實績與聯絡方式。

## 專案架構

```
Minyi/
├── app/
│   ├── __init__.py        # App Factory，初始化 Flask、資料庫
│   ├── models.py          # 資料模型：TeamMember, Work, ContactMessage, AdminUser
│   ├── forms.py           # 聯絡表單 (Flask-WTF)
│   ├── routes.py          # 路由與頁面邏輯
│   ├── templates/         # Jinja2 樣板
│   │   ├── base.html
│   │   ├── index.html     # 核心理念（首頁）
│   │   ├── team.html      # 團隊成員介紹
│   │   ├── portfolio.html # 案例實績
│   │   └── contact.html   # 聯絡方式
│   └── static/
│       ├── css/style.css
│       ├── js/main.js
│       └── images/
├── instance/               # SQLite 資料庫檔案存放處（不進版控）
├── migrations/              # 資料庫結構版本（Flask-Migrate）
├── migrate_db.py            # 建立 / 更新資料表
├── gunicorn.conf.py         # 正式環境啟動時自動執行 migrate_db
├── config.py                # 設定檔
├── run.py                   # 應用程式進入點
├── seed.py                  # 建立範例資料
├── requirements.txt
├── .env.example
└── .gitignore
```

## 快速開始

```powershell
# 1. 建立虛擬環境
python -m venv venv
venv\Scripts\activate

# 2. 安裝套件
pip install -r requirements.txt

# 3. 複製環境變數設定檔
copy .env.example .env

# 4. 建立 / 更新資料表
python migrate_db.py

# 5. （選用）建立範例資料
python seed.py

# 6. 啟動網站
python run.py
```

啟動後開啟瀏覽器造訪 http://127.0.0.1:5000

## 資料庫

預設使用 SQLite（`instance/minyi.db`），資料表由 `migrations/` 管理，執行 `python migrate_db.py` 建立或更新。

修改 `app/models.py`（例如新增欄位）後：

```powershell
flask --app run db migrate -m "說明這次的變更"   # 產生 migrations/versions/ 下的新檔案，請檢查內容
python migrate_db.py                              # 套用到本機資料庫
```

把新產生的 migration 檔一起 commit、push，Render 部署時會自動套用到正式資料庫。

### 後台帳號

後台 `/admin` 的帳號密碼存在資料表 `admin_users`（密碼只存雜湊值）。登入後可在「帳號管理」（`/admin/accounts`）檢視帳號並新增帳號。
也可以用指令新增帳號或重設密碼：

```powershell
flask --app run set-admin 帳號    # 會提示輸入兩次密碼
```

操作正式環境（Supabase）的帳號時，先把本機 `.env` 的 `DATABASE_URL` 暫時改成 Supabase 的連線字串再執行。
要停用帳號，可在 Supabase → Table Editor → `admin_users` 把 `is_active` 改為 `false`，已登入的 session 也會立即失效。

建立 `admin_users` 資料表的 migration 會把環境變數 `ADMIN_USERNAME` / `ADMIN_PASSWORD_HASH` 匯入成第一個帳號（只執行一次），
在 Supabase 上也會開啟 Row Level Security，避免密碼雜湊透過 Supabase REST API 被讀取。
未來若要更換為 PostgreSQL / MySQL，只需修改 `.env` 中的 `DATABASE_URL`。

## 功能頁面

- `/`：核心理念
- `/team`：團隊成員介紹
- `/portfolio`：案例實績
- `/contact`：聯絡方式（含表單送出，訊息會存入資料庫）

## 部署上線（Render / Railway + 自訂網域）

1. **推上 GitHub**：本機尚未是 git repo，先 `git init`、commit 後建立一個 GitHub repository 並 push 上去。
2. **建立服務**：到 Render 或 Railway 用「From GitHub repo」建立新的 Web Service，選擇這個 repository。
3. **設定啟動指令**：Start Command 填 `gunicorn run:app --bind 0.0.0.0:$PORT`（與 `Procfile` 相同）。gunicorn 會自動讀取 `gunicorn.conf.py`，每次啟動前自動更新資料庫結構。Render 的 Settings → Auto-Deploy 設為 On Commit，push 到 `main` 就會自動部署。
4. **設定環境變數**：於平台的 Environment / Variables 設定：
   - `SECRET_KEY`：換成一組隨機字串（勿沿用 `.env.example` 內的預設值）
   - `DATABASE_URL`：正式環境建議改用平台提供的 Postgres（免費方案通常有附贈），例如 `postgresql://user:password@host:5432/dbname`。若仍用 SQLite，要注意多數 PaaS 的檔案系統是暫時性的，重新部署後資料可能會消失。
5. **作品檔案存放（Supabase Storage）**：Render 的磁碟在重新部署後會清空，正式環境請將後台上傳的圖片 / 影片存到 Supabase Storage：
   - Supabase → **Storage** → **New bucket**，名稱 `works`，勾選 **Public bucket**
   - Render 環境變數新增 `SUPABASE_URL`（Project URL）、`SUPABASE_SERVICE_KEY`（secret key，勿公開）
   - 免費版單檔上限 50MB，後台影片上限也設為 50MB
6. **綁定網域**：在平台的 Custom Domain 設定輸入你的網域（例如 `www.minyi-studio.com`），平台會給一組 CNAME（或 A 記錄）目標值；接著到你購買網域的服務商（GoDaddy、Cloudflare、Gandi 等）DNS 設定頁新增該筆紀錄。DNS 生效後平台通常會自動簽發 HTTPS 憑證（Let's Encrypt）。
7. **驗證上線**：等 DNS 生效（可能數分鐘到數小時），造訪你的網域確認網站與表單功能正常。
