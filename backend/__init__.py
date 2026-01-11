from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from .config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # CORS設定: 本番環境のURLも許可（環境変数から取得可能）
    allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
    CORS(app, resources={r"/api/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Access-Control-Allow-Origin"],
        "supports_credentials": True
    }})

    db.init_app(app)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from .routes.questions import questions_bp
    app.register_blueprint(questions_bp, url_prefix='/api/questions')
    
    from .routes.health import health_bp
    app.register_blueprint(health_bp, url_prefix='/api')
    
    from .routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    return app
