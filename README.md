# 基本情報勉強アプリ

基本情報技術者試験の勉強をサポートするWebアプリケーションです。

## 機能

- ユーザー登録・ログイン機能
- 問題を解く機能
- 正答率の確認機能（今後実装予定）
- 苦手問題の分析とパーソナライズド教科書の生成（今後実装予定）

## 必要な環境

- Python 3.7以上
- Node.js 14以上
- npm または yarn

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd 基本情報勉強アプリ1
```

### 2. バックエンドのセットアップ

```bash
# バックエンドディレクトリに移動
cd backend

# 仮想環境の作成（Windows）
python -m venv venv

# 仮想環境の有効化（Windows PowerShell）
.\venv\Scripts\Activate.ps1

# 依存パッケージのインストール
pip install -r requirements.txt
```

**注意**: `requirements.txt` が存在しない場合は、以下のパッケージをインストールしてください：

```bash
pip install Flask Flask-SQLAlchemy Flask-CORS Werkzeug
```

### 3. フロントエンドのセットアップ

```bash
# プロジェクトルートに戻る
cd ..

# フロントエンドディレクトリに移動
cd frontend

# 依存パッケージのインストール
npm install
```

## データベースの初期化

### 1. データベースの作成

プロジェクトルートディレクトリで以下のコマンドを実行します：

```bash
python -m backend.create_db
```

これにより、`instance/site.db` ファイルが作成され、必要なテーブル（User、Question、Option、UserAnswer）が作成されます。

### 2. 問題データの投入

データベースに問題データを投入するには、以下のコマンドを実行します：

```bash
python -m backend.seed_data
```

これにより、7問の問題データがデータベースに投入されます。

**注意**: `seed_data.py` を実行すると、既存の問題データは全て削除され、新しく定義された問題データが投入されます。

## アプリケーションの起動

### 一括起動（推奨）

バックエンド、フロントエンド、DBを一括で起動する場合は、以下のコマンドを実行します：

```powershell
.\start_all.ps1
```

このスクリプトは以下の処理を自動的に実行します：

1. データベースの存在確認（存在しない場合は初期化）
2. 問題データの投入確認（必要に応じて）
3. バックエンドの起動（別ウィンドウ）
4. フロントエンドの起動（別ウィンドウ）

各アプリケーションは別々のPowerShellウィンドウで起動されるため、ログを個別に確認できます。
各ウィンドウを閉じることで、アプリケーションを停止できます。

### 個別起動

#### バックエンド（Flask）の起動

プロジェクトルートディレクトリで以下のコマンドを実行します：

**PowerShellスクリプトを使用する場合（推奨）:**

```powershell
.\start_backend.ps1
```

**手動で起動する場合:**

```bash
# バックエンドディレクトリに移動
cd backend

# 仮想環境の有効化（Windows PowerShell）
.\venv\Scripts\Activate.ps1

# 環境変数の設定
$env:FLASK_APP="backend"

# Flaskアプリケーションの起動
flask run --host=0.0.0.0 --port=8000
```

バックエンドは `http://127.0.0.1:8000` で起動します。

### フロントエンド（Vue.js）の起動

プロジェクトルートディレクトリで以下のコマンドを実行します：

**PowerShellスクリプトを使用する場合（推奨）:**

```powershell
.\start_frontend.ps1
```

**手動で起動する場合:**

```bash
# フロントエンドディレクトリに移動
cd frontend

# 開発サーバーの起動
npm run serve
```

フロントエンドは `http://localhost:3000` で起動します。

## アプリケーションへのアクセス

1. ブラウザで `http://localhost:3000` にアクセスします。
2. 新規登録またはログインを行います。
3. ホームページから「問題を解く」ページにアクセスできます。
4. ログイン画面からも「問題を解く」ページに直接アクセスできます。

## ディレクトリ構成

```
基本情報勉強アプリ1/
├── backend/              # バックエンド（Flask）
│   ├── __init__.py       # アプリケーションファクトリ
│   ├── app.py            # アプリケーションエントリーポイント
│   ├── config.py         # 設定ファイル
│   ├── models.py         # データベースモデル
│   ├── create_db.py      # データベース初期化スクリプト
│   ├── seed_data.py      # 問題データ投入スクリプト
│   ├── routes/           # APIルート
│   │   ├── auth.py       # 認証関連のルート
│   │   └── questions.py  # 問題関連のルート
│   ├── services/         # ビジネスロジック
│   │   ├── auth_service.py
│   │   └── question_service.py
│   └── venv/             # Python仮想環境
├── frontend/             # フロントエンド（Vue.js）
│   ├── src/
│   │   ├── views/        # ページコンポーネント
│   │   ├── components/  # 再利用可能なコンポーネント
│   │   ├── services/    # APIサービス
│   │   └── router/      # ルーティング設定
│   └── package.json
├── instance/             # データベースファイル（site.db）
├── start_all.ps1        # 一括起動スクリプト（推奨）
├── start_backend.ps1    # バックエンド起動スクリプト
└── start_frontend.ps1   # フロントエンド起動スクリプト
```

## トラブルシューティング

### バックエンドが起動しない場合

- 仮想環境が有効化されているか確認してください。
- `FLASK_APP` 環境変数が正しく設定されているか確認してください。
- ポート8000が他のプロセスで使用されていないか確認してください。

### フロントエンドが起動しない場合

- `npm install` が正常に完了しているか確認してください。
- ポート3000が他のプロセスで使用されていないか確認してください。

### CORSエラーが発生する場合

- バックエンドの `backend/__init__.py` でCORS設定が正しく行われているか確認してください。
- フロントエンドのポート（3000）がCORS設定に含まれているか確認してください。

### データベースエラーが発生する場合

- `instance/site.db` ファイルが存在するか確認してください。
- データベースを再初期化する場合は、`instance/site.db` を削除してから `python -m backend.create_db` を実行してください。

## 開発者向け情報

### APIエンドポイント

- `POST /api/auth/register` - ユーザー登録
- `POST /api/auth/login` - ログイン
- `GET /api/questions/random` - ランダムな問題を取得
- `POST /api/questions/submit_answer` - 解答を送信

### データベースモデル

- `User` - ユーザー情報
- `Question` - 問題情報
- `Option` - 選択肢情報
- `UserAnswer` - ユーザーの解答履歴

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

