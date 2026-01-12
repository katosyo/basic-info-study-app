# AWSリソースの完全再構築ガイド

このガイドでは、すべてのAWSリソースを削除し、最初から再構築する手順を説明します。

## ⚠️ 警告

この手順を実行すると、**すべてのデータが失われます**：
- データベースのデータ
- Elastic Beanstalkのアプリケーション
- CloudFrontの設定
- Amplifyの設定

## 手順

### ステップ1: 既存リソースの削除

```powershell
# 削除スクリプトを実行
.\deploy\cleanup-all.ps1

# 確認プロンプトで "yes" と入力
```

**注意**: CloudFrontの削除には時間がかかります（15-30分）。スクリプトは自動的に待機します。

### ステップ2: Amplifyアプリの削除（手動）

1. AWSコンソールにログイン
2. **Amplify** サービスに移動
3. `basic-info-study-app` を選択
4. **Actions** > **Delete app** をクリック
5. 確認して削除

### ステップ3: RDSの完全削除確認

削除が完了するまで待機（数分かかります）：

```powershell
# RDSの状態を確認
aws rds describe-db-instances --region ap-northeast-1 --query "DBInstances[?contains(DBInstanceIdentifier, 'basic-info-study')].[DBInstanceIdentifier,DBInstanceStatus]" --output table
```

### ステップ4: 再デプロイ

すべてのリソースが削除されたことを確認したら、再デプロイを開始します：

```powershell
# 1. RDSとElastic Beanstalkをデプロイ
.\deploy\deploy-all.ps1 -StackName "basic-info-study-app" -DatabasePassword "YourSecurePassword123!"

# 2. データベースの初期化
.\deploy\init-database.ps1

# 3. Amplifyアプリの再作成（GitHubリポジトリを接続）
# AWSコンソール > Amplify > New app > Host web app > GitHub
# リポジトリを選択してデプロイ

# 4. CloudFrontの設定（正しい設定で）
# 詳細は deploy/CLOUDFRONT_NEW_UI_SETUP.md を参照
```

## 再デプロイ時の重要な設定

### Elastic Beanstalk環境変数

以下の環境変数を設定してください：

```
DATABASE_URL=postgresql://postgres:YourPassword@basic-info-study-db.xxxxx.ap-northeast-1.rds.amazonaws.com:5432/postgres
SECRET_KEY=<ランダムな文字列>
FLASK_ENV=production
ALLOWED_ORIGINS=https://main.dlnofxx6dv6xm.amplifyapp.com,https://<CloudFrontドメイン>
```

### CloudFront設定のポイント

1. **Origin type**: `Elastic Load Balancer` を選択
2. **Origin domain**: Elastic BeanstalkのURL（末尾にスラッシュなし）
3. **Origin path**: 空（`/api` は含めない）
4. **Origin protocol policy**: `HTTP Only`
5. **Cache policy**: `CachingDisabled`
6. **Origin request policy**: `AllViewer`
7. **Allowed HTTP methods**: `GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE`
8. **Viewer protocol policy**: `Redirect HTTP to HTTPS`
9. **Response headers policy**: CORSヘッダーを転送するポリシーを作成

### Amplify環境変数

```
VUE_APP_API_URL=https://<CloudFrontドメイン>
```

## トラブルシューティング

### CloudFrontが504エラーを返す場合

1. Elastic Beanstalkのセキュリティグループを確認
   - CloudFrontのIPアドレス範囲（0.0.0.0/0）からのHTTPアクセスを許可
2. CloudFrontのOrigin設定を確認
   - Origin domainが正しいか
   - Origin pathが空か
3. Elastic Beanstalkのヘルスチェックを確認
   - `/api/health` エンドポイントが正常に動作しているか

### CORSエラーが発生する場合

1. Elastic Beanstalkの `ALLOWED_ORIGINS` 環境変数を確認
   - AmplifyのドメインとCloudFrontのドメインを含める
2. CloudFrontのResponse headers policyを確認
   - CORSヘッダーを転送する設定になっているか

## 完了確認

すべてのリソースが正常に動作していることを確認：

```powershell
# 1. Elastic Beanstalkの状態
aws elasticbeanstalk describe-environments --region ap-northeast-1 --query "Environments[0].[Status,Health]" --output table

# 2. RDSの状態
aws rds describe-db-instances --region ap-northeast-1 --query "DBInstances[0].DBInstanceStatus" --output text

# 3. CloudFrontの状態
aws cloudfront list-distributions --region ap-northeast-1 --query "DistributionList.Items[0].Status" --output text
```

