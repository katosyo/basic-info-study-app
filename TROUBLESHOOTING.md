# API接続エラーのトラブルシューティング

## 確認事項

### 1. Amplifyの環境変数設定

AWS Amplifyコンソールで以下を確認してください：

1. **App settings** → **Environment variables**
2. 以下の環境変数が設定されているか確認：
   ```
   Key: VUE_APP_API_URL
   Value: http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api
   ```

3. 環境変数を設定/更新したら、**必ず再デプロイ**してください：
   - Amplifyコンソールで「Redeploy this version」をクリック
   - または、GitHubにプッシュして自動デプロイを待つ

### 2. ブラウザのコンソールでエラーを確認

1. Amplifyアプリを開く（https://main.dlnofxx6dv6xm.amplifyapp.com/）
2. ブラウザの開発者ツールを開く（F12）
3. **Console**タブでエラーメッセージを確認
4. **Network**タブでAPIリクエストの状態を確認

### 3. よくあるエラーと対処法

#### CORSエラー
エラーメッセージ例：
```
Access to XMLHttpRequest at 'http://...' from origin 'https://...' has been blocked by CORS policy
```

対処法：
- Elastic Beanstalkの環境変数 `ALLOWED_ORIGINS` にAmplifyのURLが含まれているか確認
- バックエンドを再デプロイ

#### 404エラー
エラーメッセージ例：
```
GET http://.../api/questions/categories 404 (Not Found)
```

対処法：
- API URLが正しいか確認（末尾に `/api` が含まれているか）
- バックエンドのログを確認

#### ネットワークエラー
エラーメッセージ例：
```
Network Error
Failed to fetch
```

対処法：
- バックエンドが起動しているか確認
- Elastic Beanstalkのヘルスチェックを確認

### 4. バックエンドの動作確認

以下のコマンドでバックエンドが正常に動作しているか確認：

```powershell
Invoke-WebRequest -Uri "http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api/health" -UseBasicParsing
```

正常な場合、`{"status":"healthy"}` が返されます。

### 5. フロントエンドのビルド確認

Amplifyのビルドログで以下を確認：
- 環境変数 `VUE_APP_API_URL` が正しく読み込まれているか
- ビルドエラーがないか

## デバッグ手順

1. ブラウザのコンソールでエラーメッセージを確認
2. NetworkタブでAPIリクエストの詳細を確認
3. エラーメッセージを共有して、原因を特定

