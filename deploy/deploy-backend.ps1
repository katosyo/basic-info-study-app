# Backend Deployment Script
# Elastic Beanstalkにバックエンドをデプロイ

param(
    [Parameter(Mandatory=$false)]
    [string]$Region = "ap-northeast-1",
    
    [Parameter(Mandatory=$false)]
    [string]$EnvironmentName = "basic-info-study-app-env"
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Backend Deployment" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# リージョンを設定
$env:AWS_DEFAULT_REGION = $Region

# backendディレクトリに移動
if (-not (Test-Path "backend")) {
    Write-Host "Error: backend directory not found" -ForegroundColor Red
    exit 1
}

Push-Location backend

try {
    # EB CLIが初期化されているか確認
    if (-not (Test-Path ".elasticbeanstalk")) {
        Write-Host "EB CLI not initialized. Initializing..." -ForegroundColor Yellow
        Write-Host "Please follow the prompts:" -ForegroundColor Yellow
        eb init basic-info-study-app --region $Region --platform "Python 3.11"
    }
    
    # 環境が存在するか確認
    $envExists = eb status $EnvironmentName 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Environment '$EnvironmentName' not found. Creating..." -ForegroundColor Yellow
        Write-Host "This will take 5-10 minutes..." -ForegroundColor Yellow
        eb create $EnvironmentName --region $Region
    }
    
    # デプロイ
    Write-Host ""
    Write-Host "Deploying backend application..." -ForegroundColor Yellow
    eb deploy $EnvironmentName
    
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "Backend deployment completed!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    
    # 環境情報を表示
    Write-Host "Environment Info:" -ForegroundColor Cyan
    eb status $EnvironmentName
    
} finally {
    Pop-Location
}

