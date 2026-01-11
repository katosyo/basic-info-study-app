# CloudFront新UI設定ガイド

## ステップ1: Distribution options

### Distribution name
```
basic-info-study-app
```
または:
```
basic-info-study-app-cf
```
- これはCloudFrontディストリビューション全体の名前です
- タグとして保存されます
- 後で変更可能

### Description - optional
```
HTTPS access for Basic Info Study App API
```
または:
```
（空のままでもOK）
```

### Distribution type
```
Single website or app
```
- **これを選択してください**
- 各ウェブサイトやアプリケーションが独自の設定を持つ場合に使用

## ステップ2: Domain

### Route 53 managed domain - optional
```
（空のまま - スキップ）
```
- **Check domain ボタンは押さない**
- カスタムドメインは後で設定可能
- 今回はCloudFrontのデフォルトドメイン（*.cloudfront.net）を使用

## ステップ3: Tags - optional

### Key
```
Name
```
- デフォルトで「Name」が設定されている

### Value - optional
```
basic-info-study-app-origin
```
または:
```
（空のままでもOK）
```

### Add new tag
```
（追加不要 - スキップ可能）
```

## 次のステップ

「Next」または「Continue」をクリックすると、Origin設定画面に進みます。

### Origin設定画面で設定する値

**重要**: Elastic BeanstalkはS3 originではありません！

**Origin type:**
```
Elastic Load Balancer
```
- **重要**: Elastic Beanstalkは内部的にElastic Load Balancerを使用しているため、この選択が最適です
- Amazon S3、API Gateway、Elemental MediaPackage、VPC オリジン、Other は選択しない

**Origin domain:**
```
basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com
```
- `http://` や `https://` は含めない
- 末尾のスラッシュ(`/`)も含めない

**Origin path:**
```
（空のまま）
```

**Origin protocol policy:**
```
HTTP Only
```

**Name:**
```
basic-info-study-app-origin
```
（または自動生成された名前のまま）

## まとめ

**必須設定:**
- Distribution name: `basic-info-study-app`
- Distribution type: `Single website or app`
- Route 53 managed domain: **スキップ**（空のまま）

**オプション設定:**
- Description: `HTTPS access for Basic Info Study App API`（任意）
- Tags: `Name = basic-info-study-app-origin`（任意）

## 注意事項

- Distribution nameは後で変更可能です
- Route 53 managed domainはスキップして、後でカスタムドメインを設定することもできます
- Tagsはオプションなので、空のままでも問題ありません

