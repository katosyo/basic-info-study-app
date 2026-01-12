# ============================================
# AWSリソース完全削除スクリプト
# ============================================
# 警告: このスクリプトはすべてのAWSリソースを削除します
# データベースのデータも失われます

param(
    [string]$Region = "ap-northeast-1",
    [switch]$SkipConfirmation = $false
)

$ErrorActionPreference = "Stop"

Write-Host "`n=========================================" -ForegroundColor Red
Write-Host "AWSリソース完全削除スクリプト" -ForegroundColor Red
Write-Host "=========================================" -ForegroundColor Red
Write-Host "`n警告: このスクリプトは以下のリソースを削除します:" -ForegroundColor Yellow
Write-Host "  - CloudFrontディストリビューション" -ForegroundColor White
Write-Host "  - Elastic Beanstalk環境とアプリケーション" -ForegroundColor White
Write-Host "  - RDSインスタンス（データベースのデータも失われます）" -ForegroundColor White
Write-Host "  - Amplifyアプリ（オプション）" -ForegroundColor White
Write-Host "  - CloudFormationスタック" -ForegroundColor White

if (-not $SkipConfirmation) {
    $confirmation = Read-Host "`n本当に削除しますか？ (yes/no)"
    if ($confirmation -ne "yes") {
        Write-Host "`n削除をキャンセルしました。" -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "削除を開始します..." -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. CloudFrontディストリビューションの削除
Write-Host "`n【1/5】CloudFrontディストリビューションを確認中..." -ForegroundColor Yellow
try {
    $distributions = aws cloudfront list-distributions --region $Region --query "DistributionList.Items[*].[Id,DomainName,Enabled]" --output json | ConvertFrom-Json
    
    foreach ($dist in $distributions) {
        $distId = $dist[0]
        $domainName = $dist[1]
        $enabled = $dist[2]
        
        # Delete distributions related to basic-info-study or containing d2u3wft4vrii30
        if ($domainName -like "*d2u3wft4vrii30*" -or $domainName -like "*basic-info-study*") {
            Write-Host "  Disabling distribution: $distId ($domainName)" -ForegroundColor Gray
            
            # Disable first
            if ($enabled) {
                $config = aws cloudfront get-distribution-config --id $distId --region $Region --output json | ConvertFrom-Json
                $etag = $config.ETag
                
                # Set Enabled to false
                $configObj = $config.DistributionConfig | ConvertTo-Json -Depth 10 | ConvertFrom-Json
                $configObj.Enabled = $false
                $disabledConfig = $configObj | ConvertTo-Json -Depth 10 -Compress
                
                # Update configuration
                $tempFile = [System.IO.Path]::GetTempFileName()
                $disabledConfig | Out-File -FilePath $tempFile -Encoding UTF8
                
                aws cloudfront update-distribution --id $distId --if-match $etag --distribution-config "file://$tempFile" --region $Region | Out-Null
                Remove-Item $tempFile
                
                Write-Host "    Disabled. Waiting for deletion..." -ForegroundColor Gray
                
                # Wait for disabled status (max 30 minutes)
                $maxWait = 30
                $waited = 0
                do {
                    Start-Sleep -Seconds 30
                    $waited += 0.5
                    $status = aws cloudfront get-distribution --id $distId --region $Region --query "Distribution.Status" --output text 2>&1
                    $minutesText = "minutes"
                    Write-Host "    Checking status... ($($waited) $minutesText elapsed)" -ForegroundColor Gray
                } while ($status -ne "Deployed" -and $waited -lt $maxWait)
                
                # Delete
                $config = aws cloudfront get-distribution-config --id $distId --region $Region --output json | ConvertFrom-Json
                $etag = $config.ETag
                aws cloudfront delete-distribution --id $distId --if-match $etag --region $Region | Out-Null
                Write-Host "  ✓ Distribution deleted: $distId" -ForegroundColor Green
            } else {
                # Already disabled, delete directly
                $config = aws cloudfront get-distribution-config --id $distId --region $Region --output json | ConvertFrom-Json
                $etag = $config.ETag
                aws cloudfront delete-distribution --id $distId --if-match $etag --region $Region | Out-Null
                Write-Host "  ✓ Distribution deleted: $distId" -ForegroundColor Green
            }
        }
    }
} catch {
    Write-Host "  Warning: Error checking CloudFront: $_" -ForegroundColor Yellow
}

# 2. Elastic Beanstalk環境の削除
Write-Host "`n【2/5】Elastic Beanstalk環境を削除中..." -ForegroundColor Yellow
try {
    $envName = "basic-info-study-app-env"
    $appName = "basic-info-study-app"
    
    Write-Host "  Terminating environment: $envName" -ForegroundColor Gray
    aws elasticbeanstalk terminate-environment --environment-name $envName --region $Region --force-terminate 2>&1 | Out-Null
    
    Write-Host "  Waiting for termination..." -ForegroundColor Gray
    do {
        Start-Sleep -Seconds 10
        $status = aws elasticbeanstalk describe-environments --environment-names $envName --region $Region --query "Environments[0].Status" --output text 2>&1
    } while ($status -ne $null -and $status -ne "" -and $status -ne "Terminated")
    
    Write-Host "  ✓ Environment terminated: $envName" -ForegroundColor Green
    
    # Delete application
    Write-Host "  Deleting application: $appName" -ForegroundColor Gray
    aws elasticbeanstalk delete-application --application-name $appName --region $Region --terminate-env-by-force 2>&1 | Out-Null
    Write-Host "  ✓ Application deleted: $appName" -ForegroundColor Green
} catch {
    Write-Host "  Warning: Error deleting Elastic Beanstalk: $_" -ForegroundColor Yellow
}

# 3. RDSインスタンスの削除
Write-Host "`n【3/5】RDSインスタンスを削除中..." -ForegroundColor Yellow
try {
    $dbIdentifier = "basic-info-study-db"
    
    Write-Host "  Warning: Database data will be lost" -ForegroundColor Red
    Write-Host "  Deleting RDS instance: $dbIdentifier" -ForegroundColor Gray
    
    aws rds delete-db-instance `
        --db-instance-identifier $dbIdentifier `
        --skip-final-snapshot `
        --region $Region 2>&1 | Out-Null
    
    Write-Host "  Waiting for deletion (this may take several minutes)..." -ForegroundColor Gray
    do {
        Start-Sleep -Seconds 15
        $status = aws rds describe-db-instances --db-instance-identifier $dbIdentifier --region $Region --query "DBInstances[0].DBInstanceStatus" --output text 2>&1
        if ($LASTEXITCODE -ne 0) {
            break
        }
    } while ($status -ne $null -and $status -ne "")
    
    Write-Host "  ✓ RDS instance deleted: $dbIdentifier" -ForegroundColor Green
} catch {
    Write-Host "  Warning: Error deleting RDS: $_" -ForegroundColor Yellow
}

# 4. CloudFormationスタックの削除
Write-Host "`n【4/5】CloudFormationスタックを確認中..." -ForegroundColor Yellow
try {
    $stacks = aws cloudformation list-stacks --region $Region --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE ROLLBACK_COMPLETE --query "StackSummaries[?contains(StackName, `"basic-info-study`")].StackName" --output text 2>&1
    
    if ($stacks -and $stacks.Trim() -ne "") {
        $stackNames = $stacks -split "`t"
        foreach ($stackName in $stackNames) {
            if ($stackName.Trim() -ne "") {
                Write-Host "  Deleting stack: $stackName" -ForegroundColor Gray
                aws cloudformation delete-stack --stack-name $stackName --region $Region 2>&1 | Out-Null
                Write-Host "  ✓ Stack deletion started: $stackName" -ForegroundColor Green
            }
        }
    } else {
        Write-Host "  No stacks to delete" -ForegroundColor Gray
    }
} catch {
    Write-Host "  Warning: Error checking CloudFormation: $_" -ForegroundColor Yellow
}

# 5. Amplify app deletion (optional)
Write-Host "`n【5/5】Checking Amplify apps..." -ForegroundColor Yellow
Write-Host "  Note: Please delete Amplify app manually" -ForegroundColor Yellow
Write-Host '  AWS Console - Amplify - basic-info-study-app - Actions - Delete app' -ForegroundColor Gray

Write-Host "`n=========================================" -ForegroundColor Green
Write-Host "Cleanup completed" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Delete Amplify app manually (if needed)" -ForegroundColor White
Write-Host "  2. Run .\deploy\deploy-all.ps1 to redeploy" -ForegroundColor White
Write-Host "`n"

