import os

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


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = _database_url()
    # Supabase pooler 會關閉閒置連線，使用前先檢查，斷線就自動重連
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STUDIO_NAME = "明宜資訊"
    STUDIO_TAGLINE = "設計，源於用心"
    CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "hello@minyi-studio.com")

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH", "")

    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads", "works")
    ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
    ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm", "ogg", "mov"}
    MAX_IMAGE_SIZE = 5 * 1024 * 1024
    MAX_VIDEO_SIZE = 200 * 1024 * 1024
    MAX_CONTENT_LENGTH = 300 * 1024 * 1024
