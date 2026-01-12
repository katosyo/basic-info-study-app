# 最速で動かす: CloudFront無効化手順

## 目的

CloudFrontの504エラーを回避し、Elastic Beanstalkに直接接続してCORS修正を検証する。

## 手順

### ステップ1: Amplifyの環境変数を更新

1. AWSコンソール > Amplify > `basic-info-study-app` > Environment variables
2. `VUE_APP_API_URL` を以下のように設定:
   ```
   http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api
   ```
3. **Save** をクリック
4. 自動的に再デプロイが開始されます（5-10分）

**追加Tips**:
- Amplifyのビルドログを確認（Amplifyコンソール > Build settings）
- ビルドが成功しているか確認

### ステップ2: CORS修正をElastic Beanstalkにデプロイ

```powershell
# 変更をコミット・プッシュ
git add backend/
git commit -m "Fix CORS: Add OPTIONS handlers and improve CORS configuration"
git push

# Elastic Beanstalkにデプロイ
cd backend
eb deploy
```

### ステップ3: Mixed Contentエラーを一時的に無効化（テスト用）

#### Chromeの場合

1. ブラウザのアドレスバーに `chrome://flags/#block-insecure-private-network-requests` を入力
2. **Block insecure private network requests** を **Disabled** に設定
3. ブラウザを再起動

#### FirefoxやEdgeでもテスト推奨

- FirefoxやEdgeはMixed Contentの扱いが緩い場合がある
- 複数のブラウザで動作確認することで、問題の切り分けが容易

#### または、開発者ツールで警告を無視

- ConsoleタブでMixed Contentの警告を確認
- 実際の動作は確認可能（警告は表示されるがブロックされない場合あり）

**重要**: テスト後、本番では絶対にMixed Contentを残さない（ユーザー体験悪化・セキュリティ警告）

### ステップ4: 動作確認

1. AmplifyのURLにアクセス: `https://main.dlnofxx6dv6xm.amplifyapp.com`
2. ブラウザの開発者ツール（Networkタブ）を開く
3. ログインを試す
4. `/api/auth/login` のOPTIONSリクエストが成功しているか確認
5. POSTリクエストが成功しているか確認

## 確認ポイント

### OPTIONSリクエストの確認

- **ステータス**: 204または200
- **レスポンスヘッダー**:
  - `Access-Control-Allow-Origin: *` またはAmplifyドメイン
  - `Access-Control-Allow-Methods: POST, OPTIONS, ...`
  - `Access-Control-Allow-Headers: content-type, ...`

### POSTリクエストの確認

- **ステータス**: 200
- **レスポンス**: 正常なJSONレスポンス

## トラブルシューティング

### CORSエラーが続く場合

1. **Elastic Beanstalkのログを確認**:
   ```powershell
   cd backend
   eb logs
   ```

2. **環境変数を確認**:
   ```powershell
   eb printenv
   ```
   `ALLOWED_ORIGINS` にAmplifyのドメインが含まれているか確認

3. **デプロイが完了しているか確認**:
   ```powershell
   eb status
   ```

### Mixed Contentエラーが続く場合

- Chromeのフラグ設定を確認
- または、Firefoxでテスト（Mixed Contentの扱いが異なる場合がある）

## 注意事項

- ⚠️ この方法は**一時的なテスト用**です
- ⚠️ 本番環境ではHTTPS化が必要です
- ⚠️ Mixed Contentエラーは一部のブラウザでブロックされる可能性があります

## 次のステップ

動作確認後、CloudFrontの問題を解決（`SOLUTION_OPTIONS.md`の解決策2）またはALB + HTTPS構成（解決策3）に移行してください。

