# 404エラーのトラブルシューティング

## 問題

Vue.jsのSPAで、直接URLにアクセスすると404エラーが発生します。

## 原因

1. **Amplifyのデプロイがまだ完了していない**
   - 最新のデプロイが完了するまで待つ必要があります

2. **ブラウザのキャッシュ**
   - 古いバージョンがキャッシュされている可能性があります

3. **リダイレクト設定が正しく動作していない**
   - `amplify.yml`のリダイレクト設定を確認

## 解決方法

### ステップ1: Amplifyのデプロイ完了を待つ

1. [Amplifyコンソール](https://ap-northeast-1.console.aws.amazon.com/amplify/home?region=ap-northeast-1#/dlnofxx6dv6xm)にアクセス
2. 最新のデプロイジョブのStatusが「SUCCEED」になるまで待つ（3-5分）

### ステップ2: ブラウザのキャッシュをクリア

**Windows:**
- `Ctrl + Shift + R` でハードリロード
- または、`Ctrl + F5`

**Mac:**
- `Cmd + Shift + R` でハードリロード

**シークレットモード:**
- シークレットモード（プライベートブラウジング）でアクセスして確認

### ステップ3: リダイレクト設定の確認

`amplify.yml`に以下の設定が含まれていることを確認:

```yaml
redirects:
  - source: '</^[^.]+$|\.(?!(css|gif|ico|jpg|js|png|txt|svg|woff|woff2|ttf|eot)$)([^.]+$)/>'
    target: '/index.html'
    status: '200'
```

この設定により:
- すべてのルートパス（`/question-selection`など）が`index.html`にリダイレクトされます
- 静的ファイル（CSS、画像など）は除外されます

### ステップ4: 動作確認

1. Amplifyアプリにアクセス: `https://main.dlnofxx6dv6xm.amplifyapp.com`
2. 直接URLにアクセス: `https://main.dlnofxx6dv6xm.amplifyapp.com/question-selection`
3. 404エラーが発生しないことを確認

## トラブルシューティング

### エラー: デプロイが完了しても404エラーが続く

**原因**: ブラウザのキャッシュ

**解決策**:
- ブラウザのキャッシュを完全にクリア
- シークレットモードでアクセス
- 別のブラウザで確認

### エラー: 静的ファイル（CSS、画像）が読み込まれない

**原因**: リダイレクト設定が静的ファイルもリダイレクトしている

**解決策**:
- `amplify.yml`のリダイレクト設定を確認
- 静的ファイルの拡張子が除外されていることを確認

### エラー: デプロイが失敗する

**原因**: `amplify.yml`の構文エラー

**解決策**:
1. Amplifyコンソールでビルドログを確認
2. `amplify.yml`の構文を確認
3. YAMLのインデントが正しいか確認

## 現在の設定

- **リダイレクト設定**: 設定済み
- **静的ファイル除外**: 設定済み
- **Status**: デプロイ完了を待機中

## 参考

- [Amplify SPA Routing Documentation](https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html)
- [Vue Router History Mode](https://router.vuejs.org/guide/essentials/history-mode.html)

