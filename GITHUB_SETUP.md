# GitHubリポジトリの作成とプッシュ手順

## 方法1: GitHub CLIを使用（推奨）

GitHub CLIがインストールされている場合:

```powershell
gh auth login
gh repo create basic-info-study-app --public --source=. --remote=origin --push
```

## 方法2: GitHub Web UIを使用

1. https://github.com/new にアクセス
2. リポジトリ名を入力: `basic-info-study-app`
3. PublicまたはPrivateを選択
4. 「Initialize this repository with a README」は**チェックしない**（既にローカルにコードがあるため）
5. 「Create repository」をクリック
6. 以下のコマンドを実行:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/basic-info-study-app.git
git branch -M main
git push -u origin main
```

注意: `YOUR_USERNAME` を実際のGitHubユーザー名に置き換えてください。

## 認証について

GitHubへのプッシュには認証が必要です。以下のいずれかの方法を使用できます:

1. **Personal Access Token (PAT)**: 
   - GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
   - `repo` スコープを付与
   - パスワードの代わりに使用

2. **GitHub CLI**:
   ```powershell
   gh auth login
   ```

