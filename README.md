# 基本情報技術者試験 勉強アプリ

基本情報技術者試験の勉強をサポートするWebアプリケーションです。

## 機能

- 500問の問題データベース
- カテゴリ別問題選択
- 学習進捗の追跡
- 間違えた問題の復習機能
- 統計情報の表示

## 技術スタック

### フロントエンド
- Vue.js 3
- Vue Router
- Axios

### バックエンド
- Flask
- SQLAlchemy
- PostgreSQL (RDS)

### インフラ
- AWS Elastic Beanstalk (バックエンド)
- AWS Amplify (フロントエンド)
- AWS RDS PostgreSQL (データベース)

## セットアップ

### バックエンド

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### フロントエンド

```powershell
cd frontend
npm install
npm run serve
```

## デプロイ

### バックエンド (Elastic Beanstalk)

```powershell
cd backend
eb init
eb create
eb deploy
```

### フロントエンド (Amplify)

1. AWS Amplifyコンソールでアプリを作成
2. GitHubリポジトリを接続
3. 環境変数 `VUE_APP_API_URL` を設定

## ライセンス

MIT
