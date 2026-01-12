# App Runner構成のデプロイガイド

このガイドでは、App Runner + RDS + VPCコネクタ構成でアプリケーションをデプロイする手順を説明します。

## アーキテクチャ

```
Vue (静的) → Flask (API + 静的配信) → App Runner
                                      ↓
                                  VPCコネクタ
                                      ↓
                              Amazon RDS PostgreSQL
```

## 前提条件

1. AWS CLIがインストール・設定済み
2. GitHubリポジトリが準備済み
3. GitHub接続（App Runner Connections）が作成済み

## ステップ1: GitHub接続の作成

1. AWSコンソールにログイン
2. **App Runner** サービスに移動
3. **Connections** タブを開く
4. **Create connection** をクリック
5. **GitHub** を選択
6. **Authorize** をクリックしてGitHubを認証
7. 接続名を入力（例: `github-connection`）
8. **Create** をクリック
9. 接続ARNをコピー（後で使用）

## ステップ2: 既存リソースの削除

```powershell
.\deploy\cleanup-all.ps1
```

確認プロンプトで `yes` と入力します。

## ステップ3: デプロイの実行

```powershell
.\deploy\deploy-apprunner.ps1 `
    -StackName "basic-info-study-app-runner" `
    -DatabasePassword "YourSecurePassword123!" `
    -SecretKey "YourSecretKeyAtLeast16Characters" `
    -GitHubRepositoryUrl "https://github.com/your-username/your-repo" `
    -GitHubConnectionArn "arn:aws:apprunner:ap-northeast-1:123456789012:connection/github-connection/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### パラメータ説明

- `StackName`: CloudFormationスタック名
- `DatabasePassword`: RDS PostgreSQLのマスターパスワード（8文字以上）
- `SecretKey`: Flaskのシークレットキー（16文字以上）
- `GitHubRepositoryUrl`: GitHubリポジトリのURL
- `GitHubConnectionArn`: ステップ1で作成したGitHub接続のARN

### オプションパラメータ

- `DatabaseUsername`: データベースユーザー名（デフォルト: `postgres`）
- `InstanceType`: RDSインスタンスタイプ（デフォルト: `db.t3.micro`）
- `AllocatedStorage`: RDSストレージサイズ（GB、デフォルト: `20`）
- `Region`: AWSリージョン（デフォルト: `ap-northeast-1`）

## ステップ4: デプロイの確認

デプロイが完了すると、以下の情報が表示されます：

- App Runner URL: `https://xxxxxxxx.ap-northeast-1.awsapprunner.com`
- RDS Endpoint: `basic-info-study-db.xxxxx.ap-northeast-1.rds.amazonaws.com`

ブラウザでApp Runner URLにアクセスして、アプリケーションが正常に動作していることを確認してください。

## トラブルシューティング

### App Runnerが起動しない

1. App Runnerのログを確認:
   ```powershell
   aws apprunner list-operations --service-arn <SERVICE_ARN> --region ap-northeast-1
   ```

2. CloudFormationスタックのイベントを確認:
   ```powershell
   aws cloudformation describe-stack-events --stack-name basic-info-study-app-runner --region ap-northeast-1
   ```

### データベースに接続できない

1. VPCコネクタの設定を確認:
   - App RunnerサービスがVPCコネクタを使用しているか
   - セキュリティグループでRDSへのアクセスが許可されているか

2. RDSのセキュリティグループを確認:
   - App Runnerのセキュリティグループからの5432ポートへのアクセスが許可されているか

### 静的ファイルが表示されない

1. フロントエンドのビルドが成功しているか確認:
   - App Runnerのビルドログを確認
   - `frontend/dist` ディレクトリが作成されているか

2. Flaskの静的ファイル設定を確認:
   - `backend/__init__.py` の `static_folder` 設定が正しいか

## ファイル構成

デプロイに必要なファイル：

- `cloudformation/apprunner-template.yaml`: CloudFormationテンプレート
- `apprunner.yaml`: App Runner設定ファイル（オプション、API設定で上書き可能）
- `application.py`: App Runner用エントリーポイント
- `requirements.txt`: Python依存関係
- `frontend/package.json`: フロントエンド依存関係
- `deploy/deploy-apprunner.ps1`: デプロイスクリプト

## 注意事項

1. **GitHub接続**: App RunnerはGitHubリポジトリから直接デプロイするため、GitHub接続が必要です
2. **VPCコネクタ**: RDSはVPC内にあるため、VPCコネクタ経由でアクセスします
3. **静的ファイル**: Vue.jsのビルド成果物は `frontend/dist` に出力され、Flaskが配信します
4. **データベース初期化**: デプロイ後、自動的にデータベースが初期化されますが、失敗した場合は手動で `/api/admin/init-db` を呼び出してください

## 次のステップ

デプロイが完了したら：

1. アプリケーションの動作確認
2. カスタムドメインの設定（必要に応じて）
3. モニタリングとアラートの設定

