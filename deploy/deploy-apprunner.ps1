# ============================================
# App Runner構成のデプロイスクリプト
# ============================================

param(
    [Parameter(Mandatory=$true)]
    [string]$StackName = "basic-info-study-app-runner",
    
    [Parameter(Mandatory=$true)]
    [string]$DatabasePassword,
    
    [Parameter(Mandatory=$false)]
    [string]$DatabaseUsername = "postgres",
    
    [Parameter(Mandatory=$false)]
    [string]$InstanceType = "db.t3.micro",
    
    [Parameter(Mandatory=$false)]
    [int]$AllocatedStorage = 20,
    
    [Parameter(Mandatory=$true)]
    [string]$SecretKey,
    
    [Parameter(Mandatory=$true)]
    [string]$GitHubRepositoryUrl,
    
    [Parameter(Mandatory=$true)]
    [string]$GitHubConnectionArn,
    
    [string]$Region = "ap-northeast-1"
)

$ErrorActionPreference = "Stop"

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "App Runner構成のデプロイを開始します" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# CloudFormationテンプレートのパス
$templatePath = Join-Path $PSScriptRoot "..\cloudformation\apprunner-template.yaml"
$templatePath = Resolve-Path $templatePath

Write-Host "`n【1/3】CloudFormationスタックを作成中..." -ForegroundColor Yellow

# テンプレートをS3にアップロード（日本語パスの問題を回避）
$bucketName = "apprunner-deploy-templates-$(Get-Random)"
Write-Host "  テンプレートをS3にアップロード中..." -ForegroundColor Gray

try {
    # バケットを作成
    aws s3 mb "s3://$bucketName" --region $Region 2>&1 | Out-Null
    
    # テンプレートをアップロード
    $s3Key = "template.yaml"
    aws s3 cp $templatePath "s3://$bucketName/$s3Key" --region $Region 2>&1 | Out-Null
    
    $templateUrl = "https://$bucketName.s3.$Region.amazonaws.com/$s3Key"
    
    Write-Host "  テンプレートURL: $templateUrl" -ForegroundColor Gray
    
    # CloudFormationスタックを作成
    $stackParams = @(
        "ParameterKey=DatabasePassword,ParameterValue=$DatabasePassword",
        "ParameterKey=DatabaseUsername,ParameterValue=$DatabaseUsername",
        "ParameterKey=InstanceType,ParameterValue=$InstanceType",
        "ParameterKey=AllocatedStorage,ParameterValue=$AllocatedStorage",
        "ParameterKey=SecretKey,ParameterValue=$SecretKey",
        "ParameterKey=GitHubRepositoryUrl,ParameterValue=$GitHubRepositoryUrl",
        "ParameterKey=GitHubConnectionArn,ParameterValue=$GitHubConnectionArn"
    )
    
    Write-Host "  スタックを作成中（10-15分かかります）..." -ForegroundColor Gray
    
    aws cloudformation create-stack `
        --stack-name $StackName `
        --template-url $templateUrl `
        --parameters $stackParams `
        --capabilities CAPABILITY_NAMED_IAM `
        --region $Region `
        --on-failure DELETE 2>&1 | Out-Null
    
    Write-Host "  スタック作成を開始しました。完了を待機中..." -ForegroundColor Gray
    
    # スタックの完了を待機
    aws cloudformation wait stack-create-complete `
        --stack-name $StackName `
        --region $Region
    
    Write-Host "  ✓ CloudFormationスタックが作成されました" -ForegroundColor Green
    
} catch {
    Write-Host "  ✗ エラー: $_" -ForegroundColor Red
    throw
} finally {
    # S3バケットを削除
    Write-Host "  一時ファイルを削除中..." -ForegroundColor Gray
    aws s3 rm "s3://$bucketName/$s3Key" --region $Region 2>&1 | Out-Null
    aws s3 rb "s3://$bucketName" --region $Region 2>&1 | Out-Null
}

# スタックの出力を取得
Write-Host "`n【2/3】スタックの出力を取得中..." -ForegroundColor Yellow
$outputs = aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region `
    --query "Stacks[0].Outputs" `
    --output json | ConvertFrom-Json

$appRunnerUrl = ($outputs | Where-Object { $_.OutputKey -eq "AppRunnerServiceUrl" }).OutputValue
$rdsEndpoint = ($outputs | Where-Object { $_.OutputKey -eq "RDSEndpoint" }).OutputValue

Write-Host "  ✓ App Runner URL: $appRunnerUrl" -ForegroundColor Green
Write-Host "  ✓ RDS Endpoint: $rdsEndpoint" -ForegroundColor Green

# データベースの初期化
Write-Host "`n【3/3】データベースを初期化中..." -ForegroundColor Yellow
Write-Host "  App Runnerが起動するまで数分待機します..." -ForegroundColor Gray

# App Runnerのステータスを確認
$maxWait = 30
$waited = 0
do {
    Start-Sleep -Seconds 10
    $waited += 0.33
    $status = aws apprunner describe-service `
        --service-arn (aws cloudformation describe-stack-resources `
            --stack-name $StackName `
            --region $Region `
            --query "StackResources[?ResourceType=='AWS::AppRunner::Service'].PhysicalResourceId" `
            --output text) `
        --region $Region `
        --query "Service.Status" `
        --output text 2>&1
    
    Write-Host "    App Runnerステータス: $status ($([math]::Round($waited, 1)) 分経過)" -ForegroundColor Gray
} while ($status -ne "RUNNING" -and $waited -lt $maxWait)

if ($status -eq "RUNNING") {
    Write-Host "  App Runnerが起動しました。データベースを初期化します..." -ForegroundColor Green
    
    # データベース初期化APIを呼び出し
    try {
        $initUrl = "$appRunnerUrl/api/admin/init-db"
        $response = Invoke-WebRequest -Uri $initUrl -Method POST -UseBasicParsing
        
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✓ データベースの初期化が完了しました" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ データベースの初期化に失敗しました（ステータスコード: $($response.StatusCode)）" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ⚠ データベースの初期化に失敗しました: $_" -ForegroundColor Yellow
        Write-Host "  手動で初期化してください: POST $appRunnerUrl/api/admin/init-db" -ForegroundColor Gray
    }
} else {
    Write-Host "  ⚠ App Runnerの起動がタイムアウトしました" -ForegroundColor Yellow
    Write-Host "  手動で確認してください: AWS Console > App Runner" -ForegroundColor Gray
}

Write-Host "`n=========================================" -ForegroundColor Green
Write-Host "デプロイが完了しました" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "`nApp Runner URL: $appRunnerUrl" -ForegroundColor Cyan
Write-Host "RDS Endpoint: $rdsEndpoint" -ForegroundColor Cyan
Write-Host "`n"

