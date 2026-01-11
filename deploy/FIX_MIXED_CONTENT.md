# Mixed Contentエラーの解決手順

## 問題

HTTPSのフロントエンド（Amplify）からHTTPのバックエンド（Elastic Beanstalk）にアクセスしようとしているため、ブラウザがブロックしています。

## 解決方法

CloudFrontを使用してHTTPSアクセスを提供します。

### ステップ1: CloudFrontのデプロイ完了を確認

1. [CloudFrontコンソール](https://console.aws.amazon.com/cloudfront/v3/home?region=ap-northeast-1)にアクセス
2. Distribution ID: `E33QI1IDRT7XXM` を開く
3. Statusが「Deployed」になるまで待つ（5-15分）

### ステップ2: Amplifyの環境変数を更新

1. [Amplifyコンソール](https://ap-northeast-1.console.aws.amazon.com/amplify/home?region=ap-northeast-1#/dlnofxx6dv6xm)にアクセス
2. 左メニューから「環境変数」を選択
3. 「環境変数を管理」をクリック
4. `VUE_APP_API_URL` を編集または追加:
   ```
   キー: VUE_APP_API_URL
   値: https://d2u3wft4vrii30.cloudfront.net/api
   ```
5. 「保存」をクリック

### ステップ3: Amplifyアプリを再デプロイ

1. Amplifyコンソールで「ホスティング」タブを開く
2. 「Redeploy this version」をクリック
3. デプロイ完了を待つ（3-5分）

### ステップ4: 動作確認

1. Amplifyアプリにアクセス: `https://main.dlnofxx6dv6xm.amplifyapp.com`
2. ブラウザの開発者ツール（F12）を開く
3. Consoleタブでエラーがないか確認
4. NetworkタブでAPIリクエストがHTTPS経由で成功しているか確認
   - リクエストURLが `https://d2u3wft4vrii30.cloudfront.net/api/...` になっていることを確認

## 現在の設定値

- **CloudFront Domain Name**: `d2u3wft4vrii30.cloudfront.net`
- **Distribution ID**: `E33QI1IDRT7XXM`
- **Amplify環境変数**: `VUE_APP_API_URL = https://d2u3wft4vrii30.cloudfront.net/api`

## トラブルシューティング

### エラー: 環境変数が反映されない

**原因**: Amplifyアプリが再デプロイされていない

**解決策**:
- 環境変数設定後、必ず「Redeploy this version」をクリック
- デプロイが完了するまで待つ（3-5分）

### エラー: CloudFrontがデプロイされていない

**原因**: CloudFrontのデプロイに時間がかかっている

**解決策**:
- Statusが「Deployed」になるまで待つ（5-15分）
- デプロイ完了後、Amplifyの環境変数を更新

### エラー: CORSエラーが発生する

**原因**: バックエンドのCORS設定にCloudFrontのURLが含まれていない

**解決策**:
```powershell
cd backend
eb setenv ALLOWED_ORIGINS="https://main.dlnofxx6dv6xm.amplifyapp.com,https://d2u3wft4vrii30.cloudfront.net"
```

