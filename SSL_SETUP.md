# Elastic BeanstalkにSSL証明書を設定する手順

## 問題
HTTPSのAmplifyアプリからHTTPのAPIを呼び出すと、Mixed Contentエラーが発生します。

## 解決策: Elastic BeanstalkにSSL証明書を追加

### 方法1: AWS Certificate Manager (ACM) を使用（推奨）

1. **カスタムドメインを準備**
   - Route 53でドメインを取得するか、既存のドメインを使用
   - 例: `api.yourdomain.com`

2. **SSL証明書をリクエスト**
   - AWS Certificate Manager (ACM) コンソールにアクセス
   - 「証明書をリクエスト」
   - ドメイン名を入力（例: `api.yourdomain.com`）
   - DNS検証またはメール検証を完了

3. **Elastic BeanstalkにSSL証明書を設定**
   - Elastic Beanstalkコンソール → Environments → basic-info-study-app-env
   - Configuration → Load balancer
   - 「Edit」をクリック
   - 「Add listener」をクリック
   - Protocol: HTTPS、Port: 443
   - SSL certificate: 作成した証明書を選択
   - 「Apply」をクリック

4. **カスタムドメインを設定**
   - Configuration → Network
   - 「Edit」をクリック
   - 「Add custom domain」をクリック
   - ドメイン名を入力
   - Route 53でAレコードを作成（Elastic BeanstalkのCNAMEを指す）

5. **環境変数を更新**
   - Amplifyの環境変数 `VUE_APP_API_URL` を更新:
     ```
     https://api.yourdomain.com/api
     ```

### 方法2: 一時的な解決策（開発環境のみ）

セキュリティ上推奨されませんが、開発環境でのみ使用可能：

1. **Amplifyの設定でMixed Contentを許可**
   - `amplify.yml` に以下を追加:
     ```yaml
     customHeaders:
       - pattern: '**/*'
         headers:
           - key: 'Content-Security-Policy'
             value: "upgrade-insecure-requests"
     ```

2. **または、HTTPのまま使用**
   - 本番環境では推奨されません

## 推奨される解決策

**カスタムドメインとSSL証明書を設定することを強く推奨します。**

これにより：
- セキュリティが向上
- Mixed Contentエラーが解消
- 本番環境に適した構成

