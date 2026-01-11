# Elastic BeanstalkにSSL証明書を設定する（クイックガイド）

## 方法1: AWS Certificate Manager (ACM) で証明書をリクエスト

### ステップ1: SSL証明書をリクエスト

1. **AWS Certificate Manager (ACM) コンソールにアクセス**
   - https://console.aws.amazon.com/acm/home?region=ap-northeast-1
   - 「証明書をリクエスト」をクリック

2. **証明書タイプを選択**
   - 「パブリック証明書をリクエスト」を選択
   - 「次へ」をクリック

3. **ドメイン名を入力**
   - **オプションA**: カスタムドメインを使用する場合
     - 完全修飾ドメイン名（FQDN）を入力（例: `api.yourdomain.com`）
   - **オプションB**: Elastic Beanstalkのデフォルトドメインを使用する場合
     - `*.elasticbeanstalk.com` は使用できません
     - カスタムドメインが必要です

4. **検証方法を選択**
   - DNS検証（推奨）またはメール検証
   - DNS検証の場合、Route 53でCNAMEレコードを追加

5. **証明書をリクエスト**

### ステップ2: Elastic BeanstalkにSSL証明書を追加

1. **Elastic Beanstalkコンソールにアクセス**
   - https://console.aws.amazon.com/elasticbeanstalk/home?region=ap-northeast-1
   - Environments → basic-info-study-app-env

2. **Configuration → Load balancer**
   - 「Edit」をクリック

3. **HTTPSリスナーを追加**
   - 「Add listener」をクリック
   - Protocol: HTTPS
   - Port: 443
   - SSL certificate: 作成した証明書を選択
   - SSL policy: ELBSecurityPolicy-TLS-1-2-2017-01（推奨）
   - 「Apply」をクリック

4. **HTTPからHTTPSへのリダイレクト（オプション）**
   - 「Add listener」でHTTPリスナーを追加
   - 「Rules」で「Redirect to HTTPS」を設定

### ステップ3: 環境変数を更新

1. **Amplifyの環境変数を更新**
   - `VUE_APP_API_URL` をHTTPS URLに変更:
     ```
     https://api.yourdomain.com/api
     ```
   または、カスタムドメインを設定した場合:
     ```
     https://your-custom-domain.com/api
     ```

2. **CORS設定を更新**
   ```powershell
   cd backend
   eb setenv ALLOWED_ORIGINS="https://main.dlnofxx6dv6xm.amplifyapp.com,http://localhost:3000"
   ```

## 方法2: CloudFrontを使用（カスタムドメイン不要）

CloudFrontを使用してHTTPSを有効にすることもできますが、より複雑です。

## 推奨される解決策

**カスタムドメインを取得してSSL証明書を設定することを強く推奨します。**

無料ドメイン取得サービス:
- Freenom (`.tk`, `.ml`, `.ga` など)
- Namecheap（有料ですが安価）

または、既存のドメインがある場合は、サブドメインを使用できます。

