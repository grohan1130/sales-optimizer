from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    from app.routes.file_routes import file_bp
    app.register_blueprint(file_bp)

    return app 