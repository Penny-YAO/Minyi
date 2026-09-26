import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "instance", "minyi.db")
    )
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
