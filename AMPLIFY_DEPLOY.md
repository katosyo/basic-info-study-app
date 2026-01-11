# AWS Amplify デプロイ手順

## ステップ1: Amplifyアプリの作成

1. **AWS Amplifyコンソールにアクセス**
   - https://console.aws.amazon.com/amplify/ にアクセス
   - リージョンが `ap-northeast-1` であることを確認

2. **「New app」→「Host web app」をクリック**

3. **GitHubを選択**
   - 「GitHub」を選択
   - 「Authorize」をクリックしてGitHubアカウントを認証
   - リポジトリ `katosyo/basic-info-study-app` を選択
   - ブランチ `main` を選択

4. **ビルド設定の確認**
   - Amplifyが自動的に `amplify.yml` を検出します
   - 設定を確認:
     - Build settings: `amplify.yml` を使用
     - App name: `basic-info-study-app`（または任意の名前）

5. **環境変数の設定**
   - 「Environment variables」セクションを開く
   - 以下の環境変数を追加:
     ```
     VUE_APP_API_URL = http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com/api
     ```

6. **「Save and deploy」をクリック**

## ステップ2: デプロイの確認

1. ビルドプロセスが開始されます（5-10分程度）
2. ビルドが完了すると、Amplifyが自動的にURLを生成します
3. 例: `https://main.xxxxxxxxxxxx.amplifyapp.com`

## ステップ3: CORS設定の更新

AmplifyのURLが確定したら、Elastic Beanstalkの環境変数を更新します:

```powershell
cd backend
eb setenv ALLOWED_ORIGINS="https://main.xxxxxxxxxxxx.amplifyapp.com,http://localhost:3000"
```

または、AWSコンソールから:
- Elastic Beanstalk → Environments → basic-info-study-app-env
- Configuration → Software → Environment properties
- `ALLOWED_ORIGINS` を更新

## トラブルシューティング

### ビルドエラーが発生した場合
- `amplify.yml` の設定を確認
- ビルドログを確認してエラー内容を確認

### CORSエラーが発生した場合
- `ALLOWED_ORIGINS` にAmplifyのURLが正しく設定されているか確認
- バックエンドのログを確認

