from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from .config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
    app.config.from_object(config_class)

    # CORS設定: 本番環境のURLも許可（環境変数から取得可能）
    allowed_origins_str = os.environ.get('ALLOWED_ORIGINS', '*')
    
    # 本番環境では具体的なドメインを指定（セキュリティのため）
    # 開発環境では '*' を使用可能
    if allowed_origins_str == '*':
        allowed_origins = '*'
    else:
        # スペースを削除してリストに変換
        allowed_origins = [origin.strip() for origin in allowed_origins_str.split(',') if origin.strip()]
    
    # CORS設定: /api/* 以下のすべてのエンドポイントに適用
    # OPTIONS preflightリクエストも自動で処理される
    CORS(app, 
         resources={r"/api/*": {
             "origins": allowed_origins,
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
             "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
             "supports_credentials": True,
             "expose_headers": ["Content-Type", "Authorization"]
         }},
         # アプリ全体にもCORSを適用（念のため）
         supports_credentials=True
    )

    db.init_app(app)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from .routes.questions import questions_bp
    app.register_blueprint(questions_bp, url_prefix='/api/questions')
    
    from .routes.health import health_bp
    app.register_blueprint(health_bp, url_prefix='/api')
    
    from .routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # SPAルーティング: すべてのパスをindex.htmlにリダイレクト（API以外）
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_spa(path):
        if path.startswith('api/'):
            # APIリクエストは404を返す（Flaskのルーティングで処理される）
            return '', 404
        # 静的ファイルが存在する場合はそれを返す
        if path and app.static_folder:
            import os
            file_path = os.path.join(app.static_folder, path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return app.send_static_file(path)
        # それ以外はindex.htmlを返す（SPAルーティング）
        return app.send_static_file('index.html')

    return app
