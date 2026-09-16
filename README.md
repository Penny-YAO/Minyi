# Minyi Studio

個人工作室官方網站，使用 Python + Flask 建構，內容涵蓋核心理念、團隊成員介紹、案例實績與聯絡方式。

## 專案架構

```
Minyi/
├── app/
│   ├── __init__.py        # App Factory，初始化 Flask、資料庫
│   ├── models.py          # 資料模型：TeamMember, Work, ContactMessage
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

# 4. （選用）建立範例資料
python seed.py

# 5. 啟動網站
python run.py
```

啟動後開啟瀏覽器造訪 http://127.0.0.1:5000

## 資料庫

預設使用 SQLite（`instance/minyi.db`），首次啟動時會自動建立資料表。
未來若要更換為 PostgreSQL / MySQL，只需修改 `.env` 中的 `DATABASE_URL`。

## 功能頁面

- `/`：核心理念
- `/team`：團隊成員介紹
- `/portfolio`：案例實績
- `/contact`：聯絡方式（含表單送出，訊息會存入資料庫）

## 部署上線（Render / Railway + 自訂網域）

1. **推上 GitHub**：本機尚未是 git repo，先 `git init`、commit 後建立一個 GitHub repository 並 push 上去。
2. **建立服務**：到 Render 或 Railway 用「From GitHub repo」建立新的 Web Service，選擇這個 repository。
3. **設定啟動指令**：兩個平台都會讀取 `Procfile`（`web: gunicorn run:app --bind 0.0.0.0:$PORT`），通常會自動偵測，不需手動填寫。
4. **設定環境變數**：於平台的 Environment / Variables 設定：
   - `SECRET_KEY`：換成一組隨機字串（勿沿用 `.env.example` 內的預設值）
   - `DATABASE_URL`：正式環境建議改用平台提供的 Postgres（免費方案通常有附贈），例如 `postgresql://user:password@host:5432/dbname`。若仍用 SQLite，要注意多數 PaaS 的檔案系統是暫時性的，重新部署後資料可能會消失。
5. **綁定網域**：在平台的 Custom Domain 設定輸入你的網域（例如 `www.minyi-studio.com`），平台會給一組 CNAME（或 A 記錄）目標值；接著到你購買網域的服務商（GoDaddy、Cloudflare、Gandi 等）DNS 設定頁新增該筆紀錄。DNS 生效後平台通常會自動簽發 HTTPS 憑證（Let's Encrypt）。
6. **驗證上線**：等 DNS 生效（可能數分鐘到數小時），造訪你的網域確認網站與表單功能正常。
