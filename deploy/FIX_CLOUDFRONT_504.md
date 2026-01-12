# CloudFront 504エラーの解決手順

## 問題

CloudFrontがElastic Beanstalkに接続できず、504 Gateway Timeoutエラーが発生している。

## 原因の確認

### 1. Origin Protocol Policyの確認

CloudFrontコンソールで確認：
1. CloudFront > Distributions > `E33QI1IDRT7XXM`
2. **Origins** タブを開く
3. Originを選択して編集
4. **Origin protocol policy** を確認:
   - ❌ `Match Viewer`: HTTPSでEBに接続しようとして失敗
   - ✅ `HTTP Only`: HTTPでEBに接続（正しい設定）

### 2. セキュリティグループの確認

Elastic Beanstalkのセキュリティグループで：
1. EC2コンソール > Security Groups
2. Elastic Beanstalkのセキュリティグループを確認
3. **Inbound rules** を確認:
   - CloudFrontのIP範囲からのHTTP（80ポート）アクセスが許可されているか
   - または、`0.0.0.0/0` からのHTTP（80ポート）を許可（テスト用）

**ベストプラクティス（2026年現在）**:
- **AWS Managed Prefix List** を使用（推奨）:
  - Sourceで「Prefix list」を選択
  - `com.amazonaws.global.cloudfront.origin-facing` を選択
  - AWSが自動更新するため、手動メンテナンス不要
  - ルール数制限も回避可能
- テスト時は `0.0.0.0/0` でOK → 動作確認後、Prefix Listに切り替え

### 3. タイムアウト設定の確認

CloudFrontコンソールで：
1. **Behaviors** タブを開く
2. デフォルトのBehaviorを編集
3. **Origin response timeout** を確認:
   - デフォルト: 30秒
   - 推奨: 60秒以上

### 4. 直接テスト

Elastic Beanstalkに直接アクセスして動作確認：

```powershell
# ヘルスチェック
curl http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api/health

# ログインエンドポイント（OPTIONS）
curl -X OPTIONS http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api/auth/login -H "Origin: https://main.dlnofxx6dv6xm.amplifyapp.com" -v
```

## 修正手順

### ステップ1: Origin Protocol Policyを修正

1. CloudFrontコンソール > Distributions > `E33QI1IDRT7XXM`
2. **Origins** タブ > Originを選択 > **Edit**
3. **Origin protocol policy** を `HTTP Only` に設定
4. **Save changes**

### ステップ2: セキュリティグループを修正

#### オプションA: AWS Managed Prefix Listを使用（推奨・本番向け）

1. EC2コンソール > Security Groups
2. Elastic Beanstalkのセキュリティグループを選択
3. **Inbound rules** > **Edit inbound rules**
4. ルールを追加:
   - **Type**: HTTP
   - **Source**: Prefix list を選択
   - **Prefix list**: `com.amazonaws.global.cloudfront.origin-facing` を選択
   - **Description**: CloudFront origin access
5. **Save rules**

**メリット**:
- AWSが自動更新（手動メンテナンス不要）
- ルール数制限を回避
- セキュリティ向上

#### オプションB: 一時的なテスト用（0.0.0.0/0）

1. EC2コンソール > Security Groups
2. Elastic Beanstalkのセキュリティグループを選択
3. **Inbound rules** > **Edit inbound rules**
4. ルールを追加:
   - **Type**: HTTP
   - **Source**: `0.0.0.0/0` （テスト用）
5. **Save rules**

**注意**: 動作確認後、必ずPrefix List（オプションA）に切り替えてください。

### ステップ3: タイムアウトを調整

1. CloudFrontコンソール > Distributions > `E33QI1IDRT7XXM`
2. **Behaviors** タブ > デフォルトのBehaviorを選択 > **Edit**
3. **Origin response timeout** を `60` に設定
4. **Save changes**

### ステップ4: デプロイ完了を待つ

CloudFrontの変更は5-15分かかります。ステータスが `Deployed` になるまで待機。

### ステップ5: 動作確認

1. CloudFront経由でアクセス:
   ```powershell
   curl https://d2u3wft4vrii30.cloudfront.net/api/health
   ```

2. ブラウザで確認:
   - AmplifyのURLにアクセス
   - 開発者ツール（Networkタブ）で確認
   - CloudFront経由でリクエストが成功しているか確認

## トラブルシューティング

### 504エラーが続く場合

1. **CloudFrontのログを確認**:
   - CloudFrontコンソール > Distributions > `E33QI1IDRT7XXM` > **Monitoring** タブ
   - エラーレートを確認

2. **Elastic Beanstalkのログを確認**:
   ```powershell
   cd backend
   eb logs
   ```

3. **セキュリティグループを再確認**:
   - CloudFrontからのアクセスが確実に許可されているか
   - ファイアウォールルールが正しいか

### CORSエラーが続く場合

1. **Elastic Beanstalkの環境変数を確認**:
   ```powershell
   cd backend
   eb printenv
   ```
   `ALLOWED_ORIGINS` にCloudFrontのドメインが含まれているか確認

2. **CORS修正をデプロイ**:
   ```powershell
   cd backend
   eb deploy
   ```

## 確認チェックリスト

- [ ] Origin Protocol Policy: `HTTP Only`
- [ ] セキュリティグループ: CloudFrontからのアクセスを許可
- [ ] Origin Response Timeout: 60秒以上
- [ ] Elastic Beanstalkが正常に動作している（直接アクセスで確認）
- [ ] CloudFrontのステータス: `Deployed`
- [ ] CORS設定: CloudFrontのドメインを含む

## 次のステップ

CloudFrontが正常に動作したら、Amplifyの環境変数をCloudFrontのURLに戻してください：

```
VUE_APP_API_URL=https://d2u3wft4vrii30.cloudfront.net/api
```

