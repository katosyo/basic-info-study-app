# デプロイ自動化スクリプト

このディレクトリには、インフラストラクチャとアプリケーションの自動デプロイ用スクリプトが含まれています。

## 前提条件

1. **AWS CLI** がインストールされ、設定されていること
2. **EB CLI** がインストールされていること
3. **PowerShell** が利用可能であること
4. 適切なAWS権限があること

## クイックスタート

### すべてを一度にデプロイ

```powershell
.\deploy\deploy-all.ps1 `
    -StackName "basic-info-study-app" `
    -DatabasePassword "YourSecurePassword123!"
```

### ステップバイステップ

#### 1. インフラストラクチャのデプロイ

```powershell
.\deploy\deploy-infrastructure.ps1 `
    -StackName "basic-info-study-app" `
    -DatabasePassword "YourSecurePassword123!"
```

#### 2. バックエンドのデプロイ

```powershell
.\deploy\deploy-backend.ps1
```

#### 3. データベースの初期化

```powershell
.\deploy\init-database.ps1 `
    -DatabaseUrl "postgresql://postgres:password@host:5432/postgres"
```

## スクリプトの説明

### deploy-infrastructure.ps1

CloudFormationテンプレートを使用してインフラストラクチャ全体をデプロイします。

**作成されるリソース:**
- VPCとサブネット
- RDS PostgreSQLインスタンス
- Elastic Beanstalkアプリケーションと環境
- セキュリティグループ
- DBサブネットグループ

**パラメータ:**
- `StackName`: CloudFormationスタック名
- `DatabasePassword`: RDSマスターパスワード
- `SecretKey`: Flaskシークレットキー（オプション、自動生成）
- `Region`: AWSリージョン（デフォルト: ap-northeast-1）

### deploy-backend.ps1

Elastic Beanstalkにバックエンドアプリケーションをデプロイします。

**機能:**
- EB CLIの初期化（未初期化の場合）
- 環境の作成（存在しない場合）
- アプリケーションのデプロイ

### init-database.ps1

RDSデータベースを初期化し、問題データを投入します。

**パラメータ:**
- `DatabaseUrl`: データベース接続URL
- `Region`: AWSリージョン（デフォルト: ap-northeast-1）

### deploy-all.ps1

すべてのステップを順番に実行します。

**パラメータ:**
- `StackName`: CloudFormationスタック名
- `DatabasePassword`: RDSマスターパスワード
- `SecretKey`: Flaskシークレットキー（オプション）
- `SkipInfrastructure`: インフラストラクチャのデプロイをスキップ
- `SkipBackend`: バックエンドのデプロイをスキップ
- `SkipDatabase`: データベースの初期化をスキップ

## CloudFormationテンプレート

`cloudformation/template.yaml` には、すべてのAWSリソースの定義が含まれています。

**主要なリソース:**
- VPCとネットワーク設定
- RDS PostgreSQLインスタンス
- Elastic Beanstalkアプリケーションと環境
- セキュリティグループ

## 注意事項

1. **パスワード**: 強力なパスワードを使用してください
2. **コスト**: RDSとElastic Beanstalkは使用量に応じて課金されます
3. **リージョン**: すべてのリソースは同じリージョンに作成されます
4. **デプロイ時間**: インフラストラクチャのデプロイには10-20分かかります

## トラブルシューティング

### CloudFormationスタックの作成に失敗する場合

- AWS権限を確認してください
- リージョンが正しいか確認してください
- 既存のリソースと競合していないか確認してください

### バックエンドのデプロイに失敗する場合

- EB CLIが正しくインストールされているか確認してください
- `backend` ディレクトリに必要なファイルがあるか確認してください

### データベースの初期化に失敗する場合

- データベースURLが正しいか確認してください
- セキュリティグループの設定を確認してください
- 仮想環境が正しく設定されているか確認してください

