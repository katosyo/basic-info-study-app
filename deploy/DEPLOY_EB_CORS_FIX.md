# Elastic BeanstalkにCORS修正をデプロイする手順

## 現在の状況

- **App Runner**: Free Tierで利用不可（SubscriptionRequiredException）
- **Elastic Beanstalk**: 既に動作中（`basic-info-study-app-env`、Ready、Green）
- **CORS設定**: 修正済み（OPTIONSハンドラー追加、CORS設定強化）

## デプロイ手順

### ステップ1: 変更をコミット・プッシュ

```powershell
git add backend/
git commit -m "Fix CORS: Add OPTIONS handlers and improve CORS configuration"
git push
```

### ステップ2: Elastic Beanstalkにデプロイ

```powershell
cd backend
eb deploy
```

### ステップ3: デプロイ完了を待つ（5-10分）

```powershell
# ステータス確認
eb status

# ログ確認（エラーがある場合）
eb logs
```

### ステップ4: 動作確認

1. Elastic BeanstalkのURLにアクセス
2. ブラウザの開発者ツール（Networkタブ）で確認
3. `/api/auth/login` のOPTIONSリクエストが成功しているか確認

## 環境変数の確認

Elastic Beanstalkの環境変数に以下が設定されているか確認：

```
ALLOWED_ORIGINS=https://main.dlnofxx6dv6xm.amplifyapp.com,http://localhost:3000
```

設定方法：
```powershell
cd backend
eb setenv ALLOWED_ORIGINS="https://main.dlnofxx6dv6xm.amplifyapp.com,http://localhost:3000"
```

## トラブルシューティング

### CORSエラーが続く場合

1. **ブラウザのキャッシュをクリア**
2. **Elastic Beanstalkのログを確認**:
   ```powershell
   eb logs
   ```
3. **環境変数を確認**:
   ```powershell
   eb printenv
   ```

### デプロイが失敗する場合

1. **ログを確認**:
   ```powershell
   eb logs --all
   ```
2. **ヘルスチェックを確認**:
   ```powershell
   eb health
   ```

## 注意事項

- App RunnerはFree Tierで利用できないため、Elastic Beanstalkを継続使用
- CORS設定は修正済みなので、デプロイ後は正常に動作するはずです
- 本番環境では `ALLOWED_ORIGINS` を具体的なドメインに設定してください

