# CloudFront作成後の設定手順

## ステップ1: CloudFrontのデプロイ完了を待つ

1. [CloudFrontコンソール](https://console.aws.amazon.com/cloudfront/v3/home?region=ap-northeast-1)にアクセス
2. 作成したディストリビューションを開く
3. Statusが「Deployed」になるまで待つ（5-15分）
   - デプロイ中は「In Progress」と表示されます

## ステップ2: Domain Nameをコピー

1. CloudFrontコンソールでディストリビューションを開く
2. 「General」タブの「Domain name」をコピー
   - 例: `d1234567890abc.cloudfront.net`

## ステップ3: Cache settingsを編集（重要）

APIなのでキャッシュを無効化する必要があります。

### 方法1: CloudFrontコンソールから編集

1. CloudFrontコンソールでディストリビューションを開く
2. 「Behaviors」タブを開く
3. デフォルトのビヘイビアを選択して「Edit」をクリック
4. 「Cache policy」を変更:
   - 「CachingDisabled」を選択
   - または「Managed-CachingDisabled」を選択
5. 「Save changes」をクリック
6. 変更が反映されるまで数分待つ

### 方法2: AWS CLIから編集

```powershell
# Distribution IDを取得
$distId = "E1234567890ABC"  # CloudFrontコンソールから取得

# Cache policyをCachingDisabledに変更
aws cloudfront get-distribution-config --id $distId --output json > dist-config.json

# JSONファイルを編集してCachingDisabledに変更
# （複雑なため、コンソールからの編集を推奨）
```

## ステップ4: Amplifyの環境変数を更新

1. [Amplifyコンソール](https://ap-northeast-1.console.aws.amazon.com/amplify/home?region=ap-northeast-1#/dlnofxx6dv6xm)にアクセス
2. 左メニューから「環境変数」を選択
3. 「環境変数を管理」をクリック
4. `VUE_APP_API_URL` を編集または追加:
   ```
   キー: VUE_APP_API_URL
   値: https://<cloudfront-domain-name>/api
   ```
   例: `https://d1234567890abc.cloudfront.net/api`
5. 「保存」をクリック

## ステップ5: Amplifyアプリを再デプロイ

1. Amplifyコンソールで「ホスティング」タブを開く
2. 「Redeploy this version」をクリック
3. デプロイ完了を待つ（3-5分）

## ステップ6: 動作確認

1. Amplifyアプリにアクセス: `https://main.dlnofxx6dv6xm.amplifyapp.com`
2. ブラウザの開発者ツール（F12）を開く
3. Consoleタブでエラーがないか確認
4. NetworkタブでAPIリクエストがHTTPS経由で成功しているか確認
   - リクエストURLが `https://<cloudfront-domain>/api/...` になっていることを確認

## トラブルシューティング

### エラー: CloudFrontがデプロイされない

**原因**: デプロイに時間がかかっている

**解決策**:
- 5-15分待つ
- CloudFrontコンソールでStatusを確認

### エラー: APIリクエストがキャッシュされている

**原因**: Cache policyが正しく設定されていない

**解決策**:
- Cache policyを「CachingDisabled」に変更
- 変更が反映されるまで数分待つ

### エラー: CORSエラーが発生する

**原因**: バックエンドのCORS設定にCloudFrontのURLが含まれていない

**解決策**:
```powershell
cd backend
eb setenv ALLOWED_ORIGINS="https://main.dlnofxx6dv6xm.amplifyapp.com,https://<cloudfront-domain>"
```

### エラー: 404エラーが発生する

**原因**: Origin pathが間違っている

**解決策**:
- Origin pathは空のままにする
- Amplifyの環境変数で `/api` を含める: `https://<domain>/api`

