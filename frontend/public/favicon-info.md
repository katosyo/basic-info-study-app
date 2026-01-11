# Favicon作成ガイド

## 推奨方法

### 方法1: オンラインツール（Favicon Generator）

1. **Favicon.io**にアクセス
   - https://favicon.io/favicon-generator/

2. **設定**
   - Text: 「IT」または「基本情報」
   - Background: 青系（例: #2563eb）
   - Font: お好みのフォント
   - Font Size: 適切なサイズ

3. **ダウンロード**
   - 「Download」をクリック
   - `favicon.ico` と `android-chrome-192x192.png` などがダウンロードされる

4. **配置**
   - ダウンロードしたファイルを `frontend/public/` に配置
   - `favicon.ico` を `frontend/public/favicon.ico` に配置

### 方法2: シンプルなSVG Favicon

`frontend/public/favicon.svg` を作成:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" fill="#2563eb" rx="20"/>
  <text x="50" y="70" font-family="Arial, sans-serif" font-size="60" font-weight="bold" fill="white" text-anchor="middle">IT</text>
</svg>
```

### 方法3: テキストベースのFavicon

シンプルなテキストベースのfaviconを作成する場合:

1. 16x16ピクセルの画像を作成
2. 背景色: #2563eb（青）
3. テキスト: 「IT」または「基」
4. テキスト色: 白

## ファイル配置

以下のファイルを `frontend/public/` に配置:

- `favicon.ico` (16x16, 32x32)
- `favicon.svg` (推奨: スケーラブル)
- `apple-touch-icon.png` (180x180) - iOS用
- `android-chrome-192x192.png` (192x192) - Android用
- `android-chrome-512x512.png` (512x512) - Android用

## HTMLでの参照

`frontend/public/index.html` に以下を追加:

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
```

