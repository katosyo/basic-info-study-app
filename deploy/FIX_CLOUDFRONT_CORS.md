# CloudFront経由のCORSエラー解決手順

## 問題

CloudFront経由でAPIにアクセスすると、CORSエラーが発生します。

```
Access to XMLHttpRequest at 'https://d2u3wft4vrii30.cloudfront.net/api/auth/login' 
from origin 'https://main.dlnofxx6dv6xm.amplifyapp.com' 
has been blocked by CORS policy: 
Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## 原因

CloudFrontがCORSヘッダーを正しく転送していない可能性があります。

## 解決方法

### ステップ1: CloudFrontのOrigin Request Policyを確認

CloudFrontがすべてのリクエストヘッダーを転送するように設定する必要があります。

1. [CloudFrontコンソール](https://console.aws.amazon.com/cloudfront/v3/home?region=ap-northeast-1)にアクセス
2. Distribution ID: `E33QI1IDRT7XXM` を開く
3. 「Behaviors」タブを開く
4. デフォルトのビヘイビアを選択して「Edit」をクリック
5. 「Origin request policy」を確認:
   - 「AllViewer」または「Managed-AllViewer」が選択されていることを確認
   - これにより、すべてのリクエストヘッダー（Originヘッダーを含む）が転送されます

### ステップ2: CloudFrontのResponse Headers Policyを確認

CloudFrontがCORSヘッダーを正しく転送するように設定します。

1. CloudFrontコンソールで「Behaviors」タブを開く
2. デフォルトのビヘイビアを選択して「Edit」をクリック
3. 「Response headers policy」を確認:
   - 「CORS-CustomOrigin」または「CORS-S3Origin」を選択
   - または、カスタムポリシーを作成してCORSヘッダーを転送

### ステップ3: Elastic Beanstalkの環境変数を確認

バックエンドのCORS設定が正しいことを確認します。

```powershell
cd backend
eb printenv | Select-String -Pattern "ALLOWED_ORIGINS"
```

期待される値:
```
ALLOWED_ORIGINS=https://main.dlnofxx6dv6xm.amplifyapp.com,https://d2u3wft4vrii30.cloudfront.net,http://localhost:3000
```

### ステップ4: バックエンドのCORS設定を確認

`backend/__init__.py`でCORS設定が正しいことを確認します。

```python
CORS(app, resources={r"/api/*": {
    "origins": allowed_origins,
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Access-Control-Allow-Origin"],
    "supports_credentials": True
}})
```

## トラブルシューティング

### エラー: CloudFrontがCORSヘッダーを転送しない

**原因**: Origin Request Policyが正しく設定されていない

**解決策**:
- CloudFrontの「Origin request policy」を「AllViewer」に設定
- これにより、すべてのリクエストヘッダーが転送されます

### エラー: プリフライトリクエスト（OPTIONS）が失敗する

**原因**: CloudFrontがOPTIONSリクエストを正しく処理していない

**解決策**:
- CloudFrontの「Allowed HTTP methods」に「OPTIONS」が含まれていることを確認
- 「GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE」がすべて選択されていることを確認

### エラー: 環境変数が反映されない

**原因**: Elastic Beanstalkの環境更新が完了していない

**解決策**:
- Elastic BeanstalkコンソールでStatusが「Ready」になるまで待つ
- 必要に応じて環境を再起動

## 現在の設定値

- **CloudFront Domain**: `d2u3wft4vrii30.cloudfront.net`
- **Distribution ID**: `E33QI1IDRT7XXM`
- **Amplify URL**: `https://main.dlnofxx6dv6xm.amplifyapp.com`

## 参考

- [CloudFront CORS Configuration](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/header-caching.html)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)

