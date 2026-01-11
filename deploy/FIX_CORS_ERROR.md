# CORSエラーの解決手順

## 問題

CloudFront経由でAPIにアクセスしようとすると、CORSエラーが発生します。

```
Access to XMLHttpRequest at 'https://d2u3wft4vrii30.cloudfront.net/api/auth/login' 
from origin 'https://main.dlnofxx6dv6xm.amplifyapp.com' 
has been blocked by CORS policy: 
Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## 原因

バックエンドのCORS設定（`ALLOWED_ORIGINS`）にCloudFrontのURLが含まれていないためです。

## 解決方法

### ステップ1: Elastic Beanstalkの環境変数を更新

```powershell
cd backend
eb setenv ALLOWED_ORIGINS="https://main.dlnofxx6dv6xm.amplifyapp.com,https://d2u3wft4vrii30.cloudfront.net,http://localhost:3000"
```

### ステップ2: 環境更新を待つ

Elastic Beanstalkの環境が更新されるまで2-3分かかります。

[Elastic Beanstalkコンソール](https://ap-northeast-1.console.aws.amazon.com/elasticbeanstalk/home?region=ap-northeast-1#/environment/dashboard?applicationName=basic-info-study-app&environmentId=e-5dcwmufaqt)で確認:
- Statusが「Ready」になるまで待つ
- Healthが「Green」になることを確認

### ステップ3: 動作確認

1. Amplifyアプリにアクセス: `https://main.dlnofxx6dv6xm.amplifyapp.com`
2. ログインページでログインを試す
3. ブラウザの開発者ツール（F12）でCORSエラーが解消されているか確認

## 現在の設定値

- **Amplify URL**: `https://main.dlnofxx6dv6xm.amplifyapp.com`
- **CloudFront URL**: `https://d2u3wft4vrii30.cloudfront.net`
- **ローカル開発**: `http://localhost:3000`

## トラブルシューティング

### エラー: 環境変数の更新が反映されない

**原因**: Elastic Beanstalkの環境更新が完了していない

**解決策**:
- Elastic BeanstalkコンソールでStatusを確認
- Statusが「Ready」になるまで待つ
- 必要に応じて環境を再起動

### エラー: CORSエラーが続く

**原因**: 環境変数の設定が正しくない

**解決策**:
1. 環境変数を確認:
   ```powershell
   cd backend
   eb printenv | Select-String -Pattern "ALLOWED_ORIGINS"
   ```

2. 正しい値が設定されているか確認:
   ```
   ALLOWED_ORIGINS=https://main.dlnofxx6dv6xm.amplifyapp.com,https://d2u3wft4vrii30.cloudfront.net,http://localhost:3000
   ```

3. 設定が間違っている場合は再設定:
   ```powershell
   eb setenv ALLOWED_ORIGINS="https://main.dlnofxx6dv6xm.amplifyapp.com,https://d2u3wft4vrii30.cloudfront.net,http://localhost:3000"
   ```

### エラー: プリフライトリクエストが失敗する

**原因**: OPTIONSリクエストが正しく処理されていない

**解決策**:
- バックエンドのCORS設定を確認
- `backend/__init__.py`でCORS設定が正しいか確認
- `supports_credentials: True`が設定されているか確認

## 参考

- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
- [AWS Elastic Beanstalk Environment Variables](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html)

