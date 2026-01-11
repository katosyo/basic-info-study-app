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
$templatePath = Join-Path $PSScriptRoot "..\$TemplateFile"
if (-not (Test-Path $templatePath)) {
    # 相対パスで試す
    $templatePath = $TemplateFile
    if (-not (Test-Path $templatePath)) {
        Write-Host "Error: Template file not found: $TemplateFile" -ForegroundColor Red
        Write-Host "Checked paths:" -ForegroundColor Yellow
        Write-Host "  - $templatePath" -ForegroundColor Gray
        Write-Host "  - $TemplateFile" -ForegroundColor Gray
        exit 1
    }
}

Write-Host "Using template: $templatePath" -ForegroundColor Gray
$TemplateFile = $templatePath

# スタックが既に存在するか確認
try {
    $null = aws cloudformation describe-stacks --stack-name $StackName --region $Region 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Stack '$StackName' already exists. Updating..." -ForegroundColor Yellow
        $operation = "update"
    } else {
        Write-Host "Creating new stack '$StackName'..." -ForegroundColor Green
        $operation = "create"
    }
} catch {
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
    Write-Host "Creating CloudFormation stack..." -ForegroundColor Yellow
    
    # S3バケット名を生成（既存のバケットを使用または作成）
    $s3BucketName = "cfn-templates-$($Region -replace '-', '')-$([System.Guid]::NewGuid().ToString().Substring(0,8))"
    $s3TemplateKey = "templates/$StackName-template.yaml"
    
    Write-Host "Uploading template to S3..." -ForegroundColor Yellow
    
    # S3バケットを作成（存在しない場合）
    $bucketExists = aws s3 ls "s3://$s3BucketName" --region $Region 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Creating S3 bucket: $s3BucketName" -ForegroundColor Gray
        aws s3api create-bucket `
            --bucket $s3BucketName `
            --region $Region `
            --create-bucket-configuration LocationConstraint=$Region 2>&1 | Out-Null
        
        if ($LASTEXITCODE -ne 0) {
            # us-east-1の場合はLocationConstraintが不要
            aws s3api create-bucket `
                --bucket $s3BucketName `
                --region $Region 2>&1 | Out-Null
        }
    }
    
    # テンプレートファイルをS3にアップロード
    aws s3 cp $TemplateFile "s3://$s3BucketName/$s3TemplateKey" --region $Region 2>&1 | Out-Null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to upload template to S3" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Template uploaded to: s3://$s3BucketName/$s3TemplateKey" -ForegroundColor Gray
    
    try {
        # S3のURLを使用してスタックを作成
        $ErrorActionPreference = "Continue"
        $result = & aws cloudformation create-stack `
            --stack-name $StackName `
            --template-url "https://$s3BucketName.s3.$Region.amazonaws.com/$s3TemplateKey" `
            --parameters $parameters `
            --capabilities CAPABILITY_IAM `
            --region $Region `
            --output json 2>&1
        
        $exitCode = $LASTEXITCODE
        
        # 結果を表示
        Write-Host "AWS CLI Output:" -ForegroundColor Gray
        if ($result -is [System.Array]) {
            $result | ForEach-Object { Write-Host $_ -ForegroundColor Gray }
        } else {
            Write-Host $result -ForegroundColor Gray
        }
        
        # エラー出力を確認
        if ($exitCode -ne 0) {
            Write-Host "`nError: Failed to create stack" -ForegroundColor Red
            Write-Host "Exit Code: $exitCode" -ForegroundColor Red
            Write-Host "Error Output:" -ForegroundColor Red
            if ($result -is [System.Array]) {
                $result | ForEach-Object { Write-Host $_ -ForegroundColor Red }
            } else {
                Write-Host $result -ForegroundColor Red
            }
            exit 1
        }
    } catch {
        Write-Host "Exception occurred:" -ForegroundColor Red
        Write-Host "Message: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Type: $($_.Exception.GetType().FullName)" -ForegroundColor Red
        if ($_.Exception.InnerException) {
            Write-Host "Inner Exception: $($_.Exception.InnerException.Message)" -ForegroundColor Red
        }
        Write-Host "StackTrace: $($_.Exception.StackTrace)" -ForegroundColor Red
        exit 1
    } finally {
        # 一時ファイルを削除
        if (Test-Path $tempTemplatePath) {
            Remove-Item $tempTemplatePath -Force -ErrorAction SilentlyContinue
        }
    }
    
    if ($exitCode -ne 0) {
        Write-Host "Error: Failed to create stack" -ForegroundColor Red
        Write-Host "Exit Code: $exitCode" -ForegroundColor Red
        Write-Host "Error Output:" -ForegroundColor Red
        Write-Host $result -ForegroundColor Red
        
        # より詳細なエラー情報を取得
        $errorDetails = aws cloudformation describe-stack-events `
            --stack-name $StackName `
            --region $Region `
            --max-items 5 `
            --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`]' `
            --output json 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`nRecent stack events:" -ForegroundColor Yellow
            Write-Host $errorDetails -ForegroundColor Yellow
        }
        
        exit 1
    }
    
    Write-Host "Stack creation initiated successfully" -ForegroundColor Green
    Write-Host $result -ForegroundColor Gray
} else {
    Write-Host "Updating CloudFormation stack..." -ForegroundColor Yellow
    
    # S3バケット名を取得（既存のスタックから）
    $stackInfo = aws cloudformation describe-stacks --stack-name $StackName --region $Region --query 'Stacks[0].Tags[?Key==`TemplateS3Bucket`].Value' --output text 2>&1
    if ($LASTEXITCODE -eq 0 -and $stackInfo) {
        $s3BucketName = $stackInfo
        $s3TemplateKey = "templates/$StackName-template.yaml"
    } else {
        # 新しいS3バケットを作成
        $s3BucketName = "cfn-templates-$($Region -replace '-', '')-$([System.Guid]::NewGuid().ToString().Substring(0,8))"
        $s3TemplateKey = "templates/$StackName-template.yaml"
        
        Write-Host "Uploading template to S3..." -ForegroundColor Yellow
        $bucketExists = aws s3 ls "s3://$s3BucketName" --region $Region 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Creating S3 bucket: $s3BucketName" -ForegroundColor Gray
            aws s3api create-bucket `
                --bucket $s3BucketName `
                --region $Region `
                --create-bucket-configuration LocationConstraint=$Region 2>&1 | Out-Null
            
            if ($LASTEXITCODE -ne 0) {
                aws s3api create-bucket `
                    --bucket $s3BucketName `
                    --region $Region 2>&1 | Out-Null
            }
        }
        
        aws s3 cp $TemplateFile "s3://$s3BucketName/$s3TemplateKey" --region $Region 2>&1 | Out-Null
    }
    
    Write-Host "Using S3 template: s3://$s3BucketName/$s3TemplateKey" -ForegroundColor Gray
    
    try {
        # S3のURLを使用してスタックを更新
        $result = & aws cloudformation update-stack `
            --stack-name $StackName `
            --template-url "https://$s3BucketName.s3.$Region.amazonaws.com/$s3TemplateKey" `
            --parameters $parameters `
            --capabilities CAPABILITY_IAM `
            --region $Region `
            --output json 2>&1
        
        $exitCode = $LASTEXITCODE
        
        # 結果を表示
        Write-Host "AWS CLI Output:" -ForegroundColor Gray
        Write-Host $result -ForegroundColor Gray
        
        # エラー出力を確認
        if ($exitCode -ne 0) {
            # 更新が不要な場合（No updates are to be performed）は正常終了
            if ($result -match "No updates are to be performed") {
                Write-Host "No updates needed for stack '$StackName'" -ForegroundColor Yellow
                exit 0
            }
            Write-Host "`nError: Failed to update stack" -ForegroundColor Red
            Write-Host "Exit Code: $exitCode" -ForegroundColor Red
            Write-Host "Error Output:" -ForegroundColor Red
            Write-Host $result -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "Exception occurred:" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        Write-Host $_.Exception.StackTrace -ForegroundColor Red
        exit 1
    } finally {
        # 一時ファイルを削除
        if (Test-Path $tempTemplatePath) {
            Remove-Item $tempTemplatePath -Force -ErrorAction SilentlyContinue
        }
    }
    
    if ($exitCode -ne 0) {
        # 更新が不要な場合（No updates are to be performed）は正常終了
        if ($result -match "No updates are to be performed") {
            Write-Host "No updates needed for stack '$StackName'" -ForegroundColor Yellow
            exit 0
        }
        Write-Host "Error: Failed to update stack" -ForegroundColor Red
        Write-Host "Exit Code: $exitCode" -ForegroundColor Red
        Write-Host "Error Output:" -ForegroundColor Red
        Write-Host $result -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Stack update initiated successfully" -ForegroundColor Green
    Write-Host $result -ForegroundColor Gray
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

