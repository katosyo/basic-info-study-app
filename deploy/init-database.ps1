# Database Initialization Script
# RDSデータベースを初期化

param(
    [Parameter(Mandatory=$true)]
    [string]$DatabaseUrl,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "ap-northeast-1"
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Database Initialization" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# リージョンを設定
$env:AWS_DEFAULT_REGION = $Region

# DATABASE_URL環境変数を設定
$env:DATABASE_URL = $DatabaseUrl

# backendディレクトリに移動
if (-not (Test-Path "backend")) {
    Write-Host "Error: backend directory not found" -ForegroundColor Red
    exit 1
}

Push-Location backend

try {
    # 仮想環境をアクティベート
    if (Test-Path "venv\Scripts\Activate.ps1") {
        Write-Host "Activating virtual environment..." -ForegroundColor Yellow
        .\venv\Scripts\Activate.ps1
    } else {
        Write-Host "Error: Virtual environment not found" -ForegroundColor Red
        Write-Host "Please create virtual environment first:" -ForegroundColor Yellow
        Write-Host "  python -m venv venv" -ForegroundColor White
        Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
        Write-Host "  pip install -r requirements.txt" -ForegroundColor White
        exit 1
    }
    
    # データベースを初期化
    Write-Host ""
    Write-Host "Initializing database..." -ForegroundColor Yellow
    Push-Location ..
    python -m backend.init_db_remote
    Pop-Location
    
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "Database initialization completed!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host "Error: Database initialization failed" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
} finally {
    Pop-Location
}

