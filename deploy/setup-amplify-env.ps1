# Amplify環境変数設定スクリプト
# Amplifyアプリの環境変数を設定

param(
    [Parameter(Mandatory=$true)]
    [string]$AppId,
    
    [Parameter(Mandatory=$false)]
    [string]$BackendUrl = "http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "ap-northeast-1"
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Amplify Environment Variables Setup" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# リージョンを設定
$env:AWS_DEFAULT_REGION = $Region

$apiUrl = "$BackendUrl/api"

Write-Host "App ID: $AppId" -ForegroundColor Gray
Write-Host "API URL: $apiUrl" -ForegroundColor Gray
Write-Host ""

# 環境変数を設定
Write-Host "Setting environment variables..." -ForegroundColor Yellow

$envVars = @{
    "VUE_APP_API_URL" = $apiUrl
}

$envVarsJson = $envVars | ConvertTo-Json

# Amplifyの環境変数を更新
# 注意: Amplify CLIを使用する場合は、amplify env update コマンドを使用してください
# AWS CLIでは直接環境変数を設定できないため、コンソールでの設定を推奨

Write-Host ""
Write-Host "環境変数の設定が必要です:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Amplifyコンソールで以下の環境変数を設定してください:" -ForegroundColor Cyan
Write-Host ""
Write-Host "キー: VUE_APP_API_URL" -ForegroundColor White
Write-Host "値: $apiUrl" -ForegroundColor White
Write-Host ""
Write-Host "設定手順:" -ForegroundColor Yellow
Write-Host "1. AWS Amplifyコンソールにアクセス" -ForegroundColor Gray
Write-Host "2. アプリ '$AppId' を選択" -ForegroundColor Gray
Write-Host "3. 「環境変数」タブを開く" -ForegroundColor Gray
Write-Host "4. 「環境変数を管理」をクリック" -ForegroundColor Gray
Write-Host "5. 上記の環境変数を追加" -ForegroundColor Gray
Write-Host "6. 「保存」をクリック" -ForegroundColor Gray
Write-Host ""

# Amplifyアプリの情報を取得
Write-Host "Amplifyアプリの情報を取得中..." -ForegroundColor Yellow
$appInfo = aws amplify get-app --app-id $AppId --region $Region --output json 2>&1

if ($LASTEXITCODE -eq 0) {
    $app = $appInfo | ConvertFrom-Json
    Write-Host ""
    Write-Host "アプリ名: $($app.app.name)" -ForegroundColor Green
    Write-Host "デフォルトドメイン: $($app.app.defaultDomain)" -ForegroundColor Green
    Write-Host ""
    Write-Host "フロントエンドURL: https://main.$($app.app.defaultDomain)" -ForegroundColor Cyan
} else {
    Write-Host "警告: アプリ情報の取得に失敗しました" -ForegroundColor Yellow
    Write-Host $appInfo -ForegroundColor Red
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "設定完了" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

