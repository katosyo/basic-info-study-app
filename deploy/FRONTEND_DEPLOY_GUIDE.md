# フロントエンドデプロイガイド

## 現在の設定状況

- **AmplifyアプリID**: `dlnofxx6dv6xm`
- **アプリ名**: `basic-info-study-app`
- **デフォルトドメイン**: `dlnofxx6dv6xm.amplifyapp.com`
- **本番URL**: `https://main.dlnofxx6dv6xm.amplifyapp.com`
- **GitHubリポジトリ**: `katosyo/basic-info-study-app`
- **ブランチ**: `main`

## デプロイ方法

### 方法1: 自動デプロイ（推奨）

GitHubにプッシュすると自動的にデプロイが開始されます。

```powershell
# 1. 変更をステージング
git add .

# 2. コミット
git commit -m "Update frontend"

# 3. GitHubにプッシュ（自動デプロイ開始）
git push origin main
```

**メリット:**
- 簡単で確実
- デプロイ履歴が残る
- ロールバックが容易

### 方法2: Amplifyコンソールから手動デプロイ

1. [Amplifyコンソール](https://ap-northeast-1.console.aws.amazon.com/amplify/home?region=ap-northeast-1#/dlnofxx6dv6xm)にアクセス
2. 左メニューから「ホスティング」を選択
3. 「再デプロイ」ボタンをクリック
4. デプロイが完了するまで待つ（3-5分）

### 方法3: AWS CLIから手動デプロイ

```powershell
aws amplify start-job `
    --app-id dlnofxx6dv6xm `
    --branch-name main `
    --job-type RELEASE `
    --region ap-northeast-1
```

## デプロイ前の確認事項

### 1. 環境変数の設定確認

Amplifyコンソールで以下の環境変数が設定されているか確認：

**必須環境変数:**
```
VUE_APP_API_URL = http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api
```

**確認方法:**
1. Amplifyコンソール → 環境変数
2. `VUE_APP_API_URL` が存在するか確認
3. 値が正しいか確認

### 2. ビルド設定の確認

`amplify.yml` ファイルが正しく設定されているか確認：

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: frontend/dist
    files:
      - '**/*'
```

### 3. バックエンドの動作確認

バックエンドが正常に動作しているか確認：

```powershell
# ヘルスチェック
Invoke-RestMethod -Uri "http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api/health"
```

## デプロイ状況の確認

### 方法1: Amplifyコンソールで確認

1. [Amplifyコンソール](https://ap-northeast-1.console.aws.amazon.com/amplify/home?region=ap-northeast-1#/dlnofxx6dv6xm)にアクセス
2. 「ホスティング」タブでデプロイ履歴を確認
3. 各デプロイの詳細をクリックしてログを確認

### 方法2: PowerShellスクリプトで確認

```powershell
.\deploy\check-amplify-deploy.ps1
```

### 方法3: AWS CLIで確認

```powershell
aws amplify list-jobs `
    --app-id dlnofxx6dv6xm `
    --branch-name main `
    --region ap-northeast-1 `
    --max-results 5
```

## デプロイ後の確認

### 1. フロントエンドURLにアクセス

```
https://main.dlnofxx6dv6xm.amplifyapp.com
```

### 2. ブラウザの開発者ツールで確認

- F12キーで開発者ツールを開く
- 「Console」タブでエラーがないか確認
- 「Network」タブでAPIリクエストが成功しているか確認

### 3. API接続の確認

- ログイン機能が動作するか
- 問題一覧が取得できるか
- カテゴリ一覧が取得できるか

## トラブルシューティング

### ビルドエラー

**症状**: デプロイが失敗する

**対処法:**
1. Amplifyコンソールでビルドログを確認
2. `amplify.yml` の設定を確認
3. `frontend/package.json` の依存関係を確認
4. ローカルで `npm run build` が成功するか確認

### API接続エラー

**症状**: フロントエンドからAPIに接続できない

**対処法:**
1. 環境変数 `VUE_APP_API_URL` が設定されているか確認
2. バックエンドが正常に動作しているか確認
3. CORS設定を確認（バックエンドの `ALLOWED_ORIGINS`）

### Mixed Contentエラー

**症状**: HTTPSページからHTTP APIに接続できない

**対処法:**
1. `amplify.yml` の `Content-Security-Policy` ヘッダーが設定されているか確認
2. 恒久的な解決策: CloudFrontまたはElastic BeanstalkにSSL証明書を設定

### 環境変数が反映されない

**症状**: 環境変数を設定したが反映されない

**対処法:**
1. 環境変数設定後、必ず再デプロイを実行
2. ビルド時に環境変数が読み込まれているか確認
3. ブラウザのキャッシュをクリア

## よくある質問

### Q: デプロイにどのくらい時間がかかりますか？

A: 通常3-5分程度です。初回デプロイは少し長くかかる場合があります。

### Q: デプロイ中にアプリは使えますか？

A: はい、前回のデプロイが完了している場合は、デプロイ中でもアプリは使用可能です。

### Q: ロールバックはできますか？

A: はい、Amplifyコンソールで過去のデプロイを選択して「再デプロイ」をクリックできます。

### Q: 複数のブランチをデプロイできますか？

A: はい、各ブランチごとに別のURLが生成されます。

## 次のステップ

1. ✅ フロントエンドのデプロイ
2. ⏳ HTTPS設定（Mixed Contentエラー対策）
3. ⏳ カスタムドメインの設定（オプション）
4. ⏳ モニタリングとログ設定

