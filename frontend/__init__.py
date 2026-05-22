from flask import Flask

from modules.config import MAX_UPLOAD_SIZE_MB
from frontend.routes import frontend_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    app.register_blueprint(frontend_bp)
    return app
