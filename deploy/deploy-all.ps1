# Complete Deployment Script
# すべてのリソースを自動デプロイ

param(
    [Parameter(Mandatory=$true)]
    [string]$StackName,
    
    [Parameter(Mandatory=$true)]
    [string]$DatabasePassword,
    
    [Parameter(Mandatory=$false)]
    [string]$SecretKey = (New-Guid).ToString() + (New-Guid).ToString(),
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "ap-northeast-1",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipInfrastructure,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipBackend,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipDatabase
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Complete Deployment" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# ステップ1: インフラストラクチャのデプロイ
if (-not $SkipInfrastructure) {
    Write-Host "Step 1: Deploying infrastructure..." -ForegroundColor Yellow
    Write-Host ""
    & "$PSScriptRoot\deploy-infrastructure.ps1" `
        -StackName $StackName `
        -DatabasePassword $DatabasePassword `
        -SecretKey $SecretKey `
        -Region $Region
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Infrastructure deployment failed" -ForegroundColor Red
        exit 1
    }
    
    # CloudFormationの出力を取得
    $outputs = aws cloudformation describe-stacks `
        --stack-name $StackName `
        --region $Region `
        --query 'Stacks[0].Outputs' `
        --output json | ConvertFrom-Json
    
    $elasticBeanstalkUrl = ($outputs | Where-Object { $_.OutputKey -eq "ElasticBeanstalkURL" }).OutputValue
    $databaseUrl = ($outputs | Where-Object { $_.OutputKey -eq "DatabaseConnectionString" }).OutputValue
    
    Write-Host ""
    Write-Host "Infrastructure deployed successfully!" -ForegroundColor Green
    Write-Host "Elastic Beanstalk URL: $elasticBeanstalkUrl" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "Skipping infrastructure deployment..." -ForegroundColor Yellow
    # 既存のスタックから出力を取得
    $outputs = aws cloudformation describe-stacks `
        --stack-name $StackName `
        --region $Region `
        --query 'Stacks[0].Outputs' `
        --output json | ConvertFrom-Json
    
    $elasticBeanstalkUrl = ($outputs | Where-Object { $_.OutputKey -eq "ElasticBeanstalkURL" }).OutputValue
    $rdsEndpoint = ($outputs | Where-Object { $_.OutputKey -eq "RDSEndpoint" }).OutputValue
    $databaseUrl = "postgresql://postgres:$DatabasePassword@$rdsEndpoint:5432/postgres"
}

# ステップ2: バックエンドのデプロイ
if (-not $SkipBackend) {
    Write-Host ""
    Write-Host "Step 2: Deploying backend..." -ForegroundColor Yellow
    Write-Host ""
    & "$PSScriptRoot\deploy-backend.ps1" -Region $Region
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Backend deployment failed" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "Backend deployed successfully!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "Skipping backend deployment..." -ForegroundColor Yellow
}

# ステップ3: データベースの初期化
if (-not $SkipDatabase) {
    Write-Host ""
    Write-Host "Step 3: Initializing database..." -ForegroundColor Yellow
    Write-Host ""
    & "$PSScriptRoot\init-database.ps1" -DatabaseUrl $databaseUrl -Region $Region
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Database initialization failed" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "Database initialized successfully!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "Skipping database initialization..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Configure Amplify frontend:" -ForegroundColor White
Write-Host "   - Connect GitHub repository" -ForegroundColor Gray
Write-Host "   - Set environment variable:" -ForegroundColor Gray
Write-Host "     VUE_APP_API_URL = http://$elasticBeanstalkUrl/api" -ForegroundColor Gray
Write-Host "2. Update CORS settings if needed" -ForegroundColor White
Write-Host "3. Configure CloudFront for HTTPS (optional)" -ForegroundColor White
Write-Host ""

