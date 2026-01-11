# CloudFront CORSヘッダーポリシー設定ガイド

## 問題

CloudFront経由でAPIにアクセスすると、CORSエラーが発生します。これは、CloudFrontがバックエンドから返されるCORSヘッダーを転送していないためです。

## 解決方法

### ステップ1: レスポンスヘッダーポリシーを作成

1. CloudFrontコンソールで「Behaviors」タブを開く
2. デフォルトのビヘイビアを選択して「Edit」をクリック
3. 「Response headers policy」セクションで「Create response headers policy」をクリック

### ステップ2: ポリシー設定

**Policy name:**
```
CORS-Headers-Policy
```

**CORS 設定:**
- **Access-Control-Allow-Origin**: 設定しない（バックエンドから返されるヘッダーを転送）
- **Access-Control-Allow-Methods**: `GET, POST, PUT, DELETE, OPTIONS, HEAD`
- **Access-Control-Allow-Headers**: `Content-Type, Authorization, X-Requested-With`
- **Access-Control-Max-Age**: `86400`

**または、シンプルな設定:**
- 「Custom headers」で「Add header」をクリック
- 「Access-Control-Allow-Origin」を追加（値は設定しない）
- 「Access-Control-Allow-Methods」を追加（値: `GET, POST, PUT, DELETE, OPTIONS, HEAD`）
- 「Access-Control-Allow-Headers」を追加（値: `Content-Type, Authorization, X-Requested-With`）

### ステップ3: ビューワープロトコルポリシーを更新

**ビューワープロトコルポリシー:**
```
Redirect HTTP to HTTPS
```
- HTTPSにリダイレクトする設定に変更

### ステップ4: 設定を保存

1. 「Save changes」をクリック
2. 変更が反映されるまで待つ（5-15分）

## 現在の設定確認

### 正しく設定されている項目
- ✓ 許可された HTTP メソッド: `GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE`
- ✓ キャッシュポリシー: `CachingDisabled`
- ✓ オリジンリクエストポリシー: `AllViewer`

### 修正が必要な項目
- ⚠ ビューワープロトコルポリシー: `HTTP and HTTPS` → `Redirect HTTP to HTTPS` に変更
- ⚠ レスポンスヘッダーポリシー: 設定なし → CORSヘッダーを転送するポリシーを設定

## トラブルシューティング

### エラー: CORSヘッダーが転送されない

**原因**: レスポンスヘッダーポリシーが設定されていない

**解決策**:
- レスポンスヘッダーポリシーを作成して、CORSヘッダーを転送する設定にする
- バックエンドから返されるCORSヘッダーをそのまま転送する設定にする

### エラー: プリフライトリクエスト（OPTIONS）が失敗する

**原因**: Allowed HTTP methodsにOPTIONSが含まれていない

**解決策**:
- 「Allowed HTTP methods」に「OPTIONS」が含まれていることを確認
- すべてのメソッド（GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE）が選択されていることを確認

## 参考

- [CloudFront Response Headers Policy](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/adding-response-headers.html)
- [CloudFront CORS Configuration](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/header-caching.html)

