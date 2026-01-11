"""
Elastic Beanstalk用のエントリーポイント
"""
import os
import sys

# Elastic Beanstalkでは /var/app/current がルートディレクトリ
# eb deployをbackendディレクトリから実行すると、backendフォルダの内容が
# /var/app/current に配置される
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 親ディレクトリをPythonパスに追加（backendパッケージとして認識させるため）
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 現在のディレクトリもPythonパスに追加
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# backendパッケージをインポート
# eb deployをbackendディレクトリから実行すると、backendフォルダの内容が
# /var/app/currentに配置されるため、backendパッケージは存在しない
# そのため、現在のディレクトリをbackendパッケージとして扱う
try:
    # まず、backendモジュールとしてインポートを試す
    from backend import create_app
except ImportError:
    # フォールバック: 現在のディレクトリをbackendパッケージとして扱う
    # 現在のディレクトリ（/var/app/current）をbackendとして扱うため、
    # sys.pathに親ディレクトリを追加し、current_dirをbackendとして扱う
    import importlib.util
    init_path = os.path.join(current_dir, '__init__.py')
    if os.path.exists(init_path):
        # __init__.pyをbackendモジュールとして読み込む
        spec = importlib.util.spec_from_file_location("backend", init_path)
        backend_module = importlib.util.module_from_spec(spec)
        # 相対インポートをサポートするため、__package__を設定
        backend_module.__package__ = 'backend'
        backend_module.__path__ = [current_dir]
        sys.modules['backend'] = backend_module
        spec.loader.exec_module(backend_module)
        create_app = backend_module.create_app
    else:
        raise ImportError(f"Cannot find __init__.py at {init_path}")

# Elastic Beanstalkは 'application' という名前の変数を探す
application = create_app()

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000)

