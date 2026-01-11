# Amplifyフロントエンドデプロイガイド

## 前提条件

- GitHubリポジトリがAmplifyに接続されていること
- バックエンドが正常に動作していること

## 手順

### 1. Amplifyアプリの確認・作成

#### AWSコンソール経由
1. AWS Amplifyコンソールにアクセス
2. 「新しいアプリ」→「GitHubからホスト」を選択
3. GitHubリポジトリを選択: `katosyo/basic-info-study-app`
4. ブランチを選択: `main`
5. ビルド設定は `amplify.yml` を使用（自動検出）

#### AWS CLI経由
```powershell
# Amplifyアプリを作成
aws amplify create-app `
    --name basic-info-study-app `
    --region ap-northeast-1

# GitHubリポジトリを接続
aws amplify create-branch `
    --app-id <APP_ID> `
    --branch-name main `
    --region ap-northeast-1
```

### 2. 環境変数の設定

Amplifyコンソールで以下の環境変数を設定：

**必須環境変数:**
```
VUE_APP_API_URL = http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api
```

**設定方法:**
1. Amplifyコンソールでアプリを選択
2. 「環境変数」タブを開く
3. 「環境変数を管理」をクリック
4. 変数を追加:
   - キー: `VUE_APP_API_URL`
   - 値: `http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api`
5. 「保存」をクリック

### 3. CORS設定の確認

バックエンドのCORS設定でAmplifyのURLを許可する必要があります。

AmplifyのURLは以下の形式です：
```
https://<branch>.<app-id>.amplifyapp.com
```

例: `https://main.dlnofxx6dv6xm.amplifyapp.com`

バックエンドの環境変数 `ALLOWED_ORIGINS` に追加してください。

### 4. デプロイの実行

#### 自動デプロイ（推奨）
GitHubにプッシュすると自動的にデプロイされます：

```powershell
git add .
git commit -m "Update frontend configuration"
git push origin main
```

#### 手動デプロイ
Amplifyコンソールで「再デプロイ」をクリック

### 5. デプロイの確認

1. Amplifyコンソールで「ホスティング」タブを確認
2. デプロイが完了したら、URLが表示されます
3. ブラウザでアクセスして動作確認

## トラブルシューティング

### ビルドエラー
- `amplify.yml` の設定を確認
- ビルドログを確認してエラーを特定

### API接続エラー
- 環境変数 `VUE_APP_API_URL` が正しく設定されているか確認
- バックエンドのヘルスチェック: `http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api/health`

### CORSエラー
- バックエンドの `ALLOWED_ORIGINS` にAmplifyのURLが含まれているか確認
- Elastic Beanstalkの環境変数を更新して再デプロイ

### Mixed Contentエラー
- フロントエンドがHTTPS、バックエンドがHTTPの場合に発生
- 一時的な対策: `amplify.yml` の `Content-Security-Policy` ヘッダーが設定済み
- 恒久的な対策: CloudFrontまたはElastic BeanstalkにSSL証明書を設定

