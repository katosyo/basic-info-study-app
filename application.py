"""
App Runner用のエントリーポイント
"""
import os
import sys

# プロジェクトルートをPythonパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# backendパッケージをインポート
from backend import create_app

# App Runnerは 'application' という名前の変数を探す
application = create_app()

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

