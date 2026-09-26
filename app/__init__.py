import os
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "images"), exist_ok=True)
    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "videos"), exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from app.admin import admin_bp
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_now():
        return {"now": datetime.utcnow()}

    with app.app_context():
        from app import models
        db.create_all()

    return app
