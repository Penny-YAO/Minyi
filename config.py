import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "instance", "minyi.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STUDIO_NAME = "明宜資訊"
    STUDIO_TAGLINE = "設計，源於用心"
    CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "hello@minyi-studio.com")
