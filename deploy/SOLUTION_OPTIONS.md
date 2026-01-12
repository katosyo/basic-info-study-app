# 問題解決の選択肢

## 現在の問題

1. **Mixed Contentブロック**: HTTPSのAmplifyからHTTPのElastic Beanstalkにアクセス
2. **CORSエラー**: preflight OPTIONSが失敗
3. **CloudFront 504エラー**: CloudFrontがElastic Beanstalkに到達できない

## 解決策1: 最速で動かす（CloudFront無効化）

### 手順

1. **Amplifyの環境変数を更新**:
   ```
   VUE_APP_API_URL=http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api
   ```

2. **CORS修正をElastic Beanstalkにデプロイ**:
   ```powershell
   cd backend
   eb deploy
   ```

3. **動作確認**:
   - Mixed ContentはブラウザのDevToolsで一時的に無効化してテスト
   - Chrome: `chrome://flags/#block-insecure-private-network-requests` を無効化
   - または、開発者ツールのConsoleで警告を無視

### メリット
- ✅ 即座に動作確認できる
- ✅ CloudFrontの問題を回避
- ✅ CORS修正を検証できる

### デメリット
- ❌ Mixed Contentエラーが残る（本番では問題）
- ❌ HTTPS化されていない

---

## 解決策2: CloudFrontの問題を解決（推奨）

### チェック項目

#### 1. Origin Protocol Policyの確認
CloudFrontコンソールで確認：
- **Origin Protocol Policy**: `HTTP Only` に設定されているか
- `Match Viewer` だとHTTPSでEBに接続しようとして失敗

#### 2. セキュリティグループの確認
Elastic Beanstalkのセキュリティグループで：
- **推奨**: AWS Managed Prefix List `com.amazonaws.global.cloudfront.origin-facing` を使用
  - AWSが自動更新（手動メンテナンス不要）
  - ルール数制限を回避
- **テスト用**: `0.0.0.0/0` からのHTTP（80ポート）を許可
  - 動作確認後、必ずPrefix Listに切り替え

#### 3. タイムアウト設定の確認
CloudFrontの設定で：
- **Origin Response Timeout**: 30秒 → 60秒に増やす

#### 4. 直接テスト
```powershell
# Elastic Beanstalkに直接アクセスして動作確認
curl http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api/health
```

### 修正手順

1. **CloudFrontの設定を確認・修正**:
   - Origin Protocol Policy: `HTTP Only`
   - Origin Response Timeout: `60秒`
   - セキュリティグループ: CloudFrontからのアクセスを許可

2. **Amplifyの環境変数を更新**:
   ```
   VUE_APP_API_URL=https://d2u3wft4vrii30.cloudfront.net/api
   ```

3. **CORS修正をElastic Beanstalkにデプロイ**:
   ```powershell
   cd backend
   eb deploy
   ```

4. **動作確認**:
   - CloudFront経由でアクセス
   - OPTIONSリクエストが成功するか確認

### メリット
- ✅ HTTPS化される
- ✅ Mixed Contentエラーが解消
- ✅ 本番環境に適した構成

### デメリット
- ❌ 設定が複雑
- ❌ デバッグに時間がかかる可能性

---

## 解決策3: 本質的な解決（ALB + HTTPS + カスタムドメイン）

### 構成

```
Amplify (HTTPS) → CloudFront (HTTPS) → ALB (HTTPS) → EB (HTTP内部)
```

### 手順（2026年現在の標準手順）

1. **Elastic Beanstalk環境をLoad Balancedに変更**
   - コンソールまたは `.ebextensions` で設定
   - Single instance → Application Load Balancer に変更

2. **Route 53でカスタムドメインを取得/ホストゾーン作成**
   - 例: `api.basicinfo.app`
   - ホストゾーンを作成

3. **ACM（us-east-1推奨）でSSL証明書をリクエスト**
   - DNS検証を選択（Route 53自動検証が可能）
   - 証明書ARNをコピー

4. **`.ebextensions/https-alb.config` ファイルを作成**
   ```yaml
   option_settings:
     aws:elbv2:listener:443:
       ListenerEnabled: 'true'
       Protocol: HTTPS
       SSLCertificateArns: arn:aws:acm:us-east-1:123456789012:certificate/xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```
   - `backend/.ebextensions/` に配置
   - デプロイ: `eb deploy`

5. **CloudFrontのOriginをALBのDNS（HTTPS Only）に変更**
   - Origin Protocol Policy: `HTTPS Only`
   - Origin domain: ALBのDNS名

6. **CORSのALLOWED_ORIGINSにカスタムドメインを追加**
   ```powershell
   eb setenv ALLOWED_ORIGINS="https://main.dlnofxx6dv6xm.amplifyapp.com,https://api.basicinfo.app"
   ```

### コスト
- ALB: 約$16/月
- カスタムドメイン: 約$10-15/年
- CloudFront: 使用量に応じて

### メリット
- ✅ 完全なHTTPS化
- ✅ 本番環境に最適
- ✅ スケーラブル

### デメリット
- ❌ コストがかかる（Free Tier外）
- ❌ 設定が複雑
- ❌ 時間がかかる

---

## 推奨アプローチ

### 短期（今すぐ動かす）
**解決策1**: CloudFrontを無効化して直接接続
- CORS修正を検証
- Mixed Contentは一時的にDevToolsで無視

### 中期（1-2週間）
**解決策2**: CloudFrontの問題を解決
- Origin Protocol Policyを修正
- セキュリティグループを確認
- タイムアウトを調整

### 長期（本番リリース時）
**解決策3**: ALB + HTTPS + カスタムドメイン
- 完全なHTTPS化
- 本番環境に適した構成

---

## 次のステップ

1. **解決策1を実行**（最速で動作確認）
2. **解決策2を並行して進める**（CloudFrontの設定を確認）
3. **動作確認後、解決策3を検討**（本番リリース時）

