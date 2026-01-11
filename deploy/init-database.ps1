# Database Initialization Script
# RDSデータベースを初期化（APIエンドポイント経由）

param(
    [Parameter(Mandatory=$false)]
    [string]$BackendUrl = "http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com",
    
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

Write-Host "Backend URL: $BackendUrl" -ForegroundColor Gray
Write-Host ""

# APIエンドポイント経由でデータベースを初期化
try {
    Write-Host "Initializing database via API endpoint..." -ForegroundColor Yellow
    
    $initUrl = "$BackendUrl/api/admin/init-db"
    Write-Host "Calling: $initUrl" -ForegroundColor Gray
    
    $response = Invoke-RestMethod -Uri $initUrl -Method Post -ContentType "application/json" -ErrorAction Stop
    
    Write-Host ""
    Write-Host "Response:" -ForegroundColor Gray
    Write-Host ($response | ConvertTo-Json -Depth 10) -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "Database initialization completed!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "Error: Database initialization failed" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody" -ForegroundColor Red
    } else {
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
    exit 1
}

