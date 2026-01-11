# Infrastructure Deployment Script
# CloudFormationテンプレートを使用してインフラをデプロイ

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
    [string]$TemplateFile = "cloudformation/template.yaml"
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Infrastructure Deployment" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# リージョンを設定
$env:AWS_DEFAULT_REGION = $Region

# テンプレートファイルの存在確認
if (-not (Test-Path $TemplateFile)) {
    Write-Host "Error: Template file not found: $TemplateFile" -ForegroundColor Red
    exit 1
}

# スタックが既に存在するか確認
$existingStack = aws cloudformation describe-stacks --stack-name $StackName --region $Region 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Stack '$StackName' already exists. Updating..." -ForegroundColor Yellow
    $operation = "update"
} else {
    Write-Host "Creating new stack '$StackName'..." -ForegroundColor Green
    $operation = "create"
}

# CloudFormationスタックを作成/更新
Write-Host ""
Write-Host "Deploying CloudFormation stack..." -ForegroundColor Yellow
Write-Host "Stack Name: $StackName" -ForegroundColor Cyan
Write-Host "Region: $Region" -ForegroundColor Cyan
Write-Host ""

$parameters = @(
    "ParameterKey=DatabasePassword,ParameterValue=$DatabasePassword",
    "ParameterKey=SecretKey,ParameterValue=$SecretKey"
)

if ($operation -eq "create") {
    $result = aws cloudformation create-stack `
        --stack-name $StackName `
        --template-body file://$TemplateFile `
        --parameters $parameters `
        --capabilities CAPABILITY_IAM `
        --region $Region `
        --output json
} else {
    $result = aws cloudformation update-stack `
        --stack-name $StackName `
        --template-body file://$TemplateFile `
        --parameters $parameters `
        --capabilities CAPABILITY_IAM `
        --region $Region `
        --output json
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to $operation stack" -ForegroundColor Red
    Write-Host $result -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Stack $operation initiated. Waiting for completion..." -ForegroundColor Yellow
Write-Host "This may take 10-20 minutes..." -ForegroundColor Yellow
Write-Host ""

# スタックの完了を待つ
aws cloudformation wait stack-$($operation)-complete `
    --stack-name $StackName `
    --region $Region

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Stack $operation failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Stack $operation completed successfully!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# 出力を表示
Write-Host "Stack Outputs:" -ForegroundColor Cyan
aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region `
    --query 'Stacks[0].Outputs' `
    --output table

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Deploy backend application to Elastic Beanstalk" -ForegroundColor White
Write-Host "2. Initialize database" -ForegroundColor White
Write-Host "3. Configure Amplify frontend" -ForegroundColor White
Write-Host ""

