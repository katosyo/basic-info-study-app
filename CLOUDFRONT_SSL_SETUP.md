# CloudFrontを使用してHTTPSを有効にする（カスタムドメイン不要）

## 概要
CloudFrontを使用してElastic BeanstalkのAPIにHTTPSアクセスを提供します。カスタムドメインは不要です。

## ステップ1: CloudFrontディストリビューションを作成

1. **CloudFrontコンソールにアクセス**
   - https://console.aws.amazon.com/cloudfront/v3/home?region=ap-northeast-1
   - 「Create distribution」をクリック

2. **Origin設定**
   - **Origin domain**: Elastic Beanstalkのエンドポイントを選択
     - `basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com`
   - **Origin path**: 空のまま（`/api`は含めない）
   - **Name**: 自動生成される（変更不要）
   - **Origin protocol policy**: HTTP Only（Elastic BeanstalkはHTTPのみのため）

3. **Default cache behavior設定**
   - **Viewer protocol policy**: Redirect HTTP to HTTPS
   - **Allowed HTTP methods**: GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE
   - **Cache policy**: CachingDisabled（APIなのでキャッシュしない）
   - **Origin request policy**: AllViewer（すべてのリクエストを転送）

4. **Distribution settings**
   - **Price class**: Use all edge locations (best performance)
   - **Alternate domain names (CNAMEs)**: 空のまま（カスタムドメイン不要）
   - **SSL certificate**: Default CloudFront certificate (使用可能)
   - **Default root object**: 空のまま

5. **「Create distribution」をクリック**

## ステップ2: CloudFrontのデプロイを待つ

- デプロイには5-15分かかります
- Statusが「Deployed」になるまで待ちます

## ステップ3: Amplifyの環境変数を更新

1. **CloudFrontのURLを取得**
   - CloudFrontコンソールで作成したディストリビューションを開く
   - **Domain name**をコピー（例: `d1234567890abc.cloudfront.net`）

2. **Amplifyの環境変数を更新**
   - AWS Amplifyコンソール → App settings → Environment variables
   - `VUE_APP_API_URL` を更新:
     ```
     https://d1234567890abc.cloudfront.net/api
     ```
   - 注意: 末尾に `/api` を含める

3. **再デプロイ**
   - 「Redeploy this version」をクリック

## ステップ4: CORS設定を確認

CORS設定は既に正しく設定されているはずです。確認:

```powershell
cd backend
eb printenv | Select-String -Pattern "ALLOWED_ORIGINS"
```

AmplifyのURLが含まれていることを確認してください。

## ステップ5: 動作確認

1. Amplifyアプリを開く
2. ブラウザのコンソールでエラーがないか確認
3. APIリクエストがHTTPS経由で動作することを確認

## 注意事項

- CloudFrontのデプロイには時間がかかります（5-15分）
- CloudFrontは無料枠がありますが、使用量に応じて課金されます
- APIのレスポンスがキャッシュされないように設定しています

