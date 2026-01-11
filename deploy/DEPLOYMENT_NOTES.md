# デプロイメントに関する注意事項

## 既存リソースとの競合

CloudFormationテンプレートを実行する際、以下の既存リソースと競合する可能性があります：

### Elastic Beanstalk Application
- **既存リソース**: `basic-info-study-app`
- **対処法**: 
  1. 既存のアプリケーションを削除する
  2. または、CloudFormationテンプレートで別の名前を使用する（`basic-info-study-app-cfn`）

### RDS Instance
- **既存リソース**: `basic-info-study-db`
- **対処法**:
  1. 既存のRDSインスタンスを削除する
  2. または、CloudFormationテンプレートで別の名前を使用する

## 推奨されるアプローチ

### オプション1: 既存リソースを削除してからデプロイ（推奨）

```powershell
# 既存のElastic Beanstalk環境を削除
cd backend
eb terminate basic-info-study-app-env

# 既存のRDSインスタンスを削除（注意：データが失われます）
aws rds delete-db-instance --db-instance-identifier basic-info-study-db --skip-final-snapshot --region ap-northeast-1

# その後、CloudFormationでデプロイ
.\deploy\deploy-all.ps1 -StackName "basic-info-study-app" -DatabasePassword "YourPassword123!"
```

### オプション2: CloudFormationテンプレートを修正して既存リソースを使用

既存のリソースをCloudFormationで管理する場合は、テンプレートを修正して既存リソースをインポートする必要があります。

### オプション3: 既存リソースをそのまま使用

CloudFormationを使用せず、既存のリソースをそのまま使用して、バックエンドのみをデプロイすることもできます。

