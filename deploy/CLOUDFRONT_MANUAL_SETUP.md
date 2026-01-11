# CloudFront手動設定ガイド（詳細版）

## CloudFrontコンソールURL
https://console.aws.amazon.com/cloudfront/v3/home?region=ap-northeast-1

## ステップ1: Create distribution をクリック

## ステップ2: Origin設定

### Origin 1

**Origin domain:**
```
basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com
```
- ドロップダウンから選択するか、直接入力
- **重要**: `http://` や `https://` は含めない

**Origin path:**
```
（空のまま）
```
- `/api` は含めない（CloudFrontがすべてのパスを転送するため）

**Name:**
```
（自動生成されるので変更不要）
```
- デフォルトのままでOK

**Origin protocol policy:**
```
HTTP Only
```
- Elastic BeanstalkはHTTPのみのため

**HTTP port:**
```
80
```
- デフォルト値

**HTTPS port:**
```
443
```
- デフォルト値（Origin protocol policyがHTTP Onlyでも設定は必要）

**Origin SSL protocols:**
```
TLSv1.2
```
- デフォルトで選択されている

## ステップ3: Default cache behavior設定

**Path pattern:**
```
Default (*)
```
- デフォルトのままでOK（すべてのパスに適用）

**Viewer protocol policy:**
```
Redirect HTTP to HTTPS
```
- **重要**: HTTPSにリダイレクトする設定

**Allowed HTTP methods:**
```
GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE
```
- すべてのHTTPメソッドを許可（APIなので）

**Cache policy:**
```
CachingDisabled
```
- **重要**: APIなのでキャッシュを無効化
- または「Managed-CachingDisabled」を選択

**Origin request policy:**
```
AllViewer
```
- すべてのリクエストヘッダーとクエリ文字列を転送
- または「Managed-AllViewer」を選択

**Response headers policy:**
```
（デフォルトのままでOK）
```

**Compress objects automatically:**
```
Yes
```
- パフォーマンス向上のため

## ステップ4: Distribution settings

**Price class:**
```
Use all edge locations (best performance)
```
- または「Use only North America and Europe」でコスト削減可能

**Alternate domain names (CNAMEs):**
```
（空のまま）
```
- カスタムドメインを使用しない場合は空のまま

**SSL certificate:**
```
Default CloudFront certificate (*.cloudfront.net)
```
- **重要**: デフォルトのCloudFront証明書を使用（カスタムドメイン不要）

**Default root object:**
```
（空のまま）
```
- APIなので不要

**Comment:**
```
HTTPS access for Basic Info Study App API
```
- 任意（説明用）

**Web Application Firewall (WAF):**
```
（デフォルトのままでOK）
```

## ステップ5: Create distribution をクリック

## ステップ6: デプロイ完了を待つ

- Statusが「Deployed」になるまで5-15分かかります
- デプロイ中は「In Progress」と表示されます

## ステップ7: Domain Nameを確認

デプロイ完了後、以下の情報を確認：

**Distribution ID:**
```
（例: E1234567890ABC）
```

**Domain name:**
```
（例: d1234567890abc.cloudfront.net）
```
- このURLをAmplifyの環境変数で使用します

## ステップ8: Amplifyの環境変数を更新

1. [Amplifyコンソール](https://ap-northeast-1.console.aws.amazon.com/amplify/home?region=ap-northeast-1#/dlnofxx6dv6xm)にアクセス
2. 左メニューから「環境変数」を選択
3. 「環境変数を管理」をクリック
4. `VUE_APP_API_URL` を編集または追加：
   ```
   キー: VUE_APP_API_URL
   値: https://<cloudfront-domain-name>/api
   ```
   例: `https://d1234567890abc.cloudfront.net/api`
5. 「保存」をクリック

## ステップ9: Amplifyアプリを再デプロイ

1. Amplifyコンソールで「ホスティング」タブを開く
2. 「Redeploy this version」をクリック
3. デプロイ完了を待つ（3-5分）

## ステップ10: 動作確認

1. Amplifyアプリにアクセス: `https://main.dlnofxx6dv6xm.amplifyapp.com`
2. ブラウザの開発者ツール（F12）を開く
3. Consoleタブでエラーがないか確認
4. NetworkタブでAPIリクエストがHTTPS経由で成功しているか確認

## トラブルシューティング

### エラー: Origin domainが見つからない

**原因**: Origin domainの入力が間違っている

**解決策**:
- `http://` や `https://` を含めていないか確認
- Elastic Beanstalkのエンドポイントが正しいか確認

### エラー: CORSエラーが発生する

**原因**: バックエンドのCORS設定にCloudFrontのURLが含まれていない

**解決策**:
```powershell
cd backend
eb setenv ALLOWED_ORIGINS="https://main.dlnofxx6dv6xm.amplifyapp.com,https://d1234567890abc.cloudfront.net"
```

### エラー: APIリクエストがキャッシュされている

**原因**: Cache policyが正しく設定されていない

**解決策**:
- CloudFrontコンソールで「Cache policy」を「CachingDisabled」に設定
- または「Managed-CachingDisabled」を選択

### エラー: 404エラーが発生する

**原因**: Origin pathが間違っている

**解決策**:
- Origin pathは空のままにする（`/api` は含めない）
- Amplifyの環境変数で `/api` を含める: `https://<domain>/api`

## 参考情報

- [CloudFront公式ドキュメント](https://docs.aws.amazon.com/cloudfront/)
- [Elastic Beanstalkエンドポイント確認](http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api/health)

