import os
from urllib.parse import urlsplit

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


def _database_url():
    url = os.environ.get("DATABASE_URL", "").strip()
    if not url:
        return "sqlite:///" + os.path.join(basedir, "instance", "minyi.db")
    # 明確指定使用 psycopg（第 3 版）驅動，避免不同 SQLAlchemy 版本預設的驅動不同
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


def _supabase_url():
    url = os.environ.get("SUPABASE_URL", "").strip()
    if not url:
        return ""
    # 只保留 https://xxxx.supabase.co，避免誤填成 .../storage/v1/s3 或 .../rest/v1/ 等 API 網址
    parts = urlsplit(url if "://" in url else "https://" + url)
    return f"{parts.scheme}://{parts.netloc}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = _database_url()
    # Supabase pooler 會關閉閒置連線，使用前先檢查，斷線就自動重連
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STUDIO_NAME = "明宜資訊"
    STUDIO_TAGLINE = "設計，源於用心"
    CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "hello@minyi-studio.com")

    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads", "works")
    ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
    ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm", "ogg", "mov"}
    MAX_IMAGE_SIZE = 5 * 1024 * 1024
    MAX_VIDEO_SIZE = 50 * 1024 * 1024
    MAX_CONTENT_LENGTH = 60 * 1024 * 1024

    # 有設定時作品檔案上傳至 Supabase Storage，未設定則存在本機 static/uploads
    SUPABASE_URL = _supabase_url()
    SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "").strip()
    SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "works").strip()
