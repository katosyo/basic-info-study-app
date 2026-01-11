# CloudFrontディストリビューション作成スクリプト
# Elastic BeanstalkのAPIにHTTPSアクセスを提供

param(
    [Parameter(Mandatory=$false)]
    [string]$BackendUrl = "http://basic-info-study-app-env.eba-vdpqbbpm.ap-northeast-1.elasticbeanstalk.com",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "ap-northeast-1"
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "CloudFront Setup for HTTPS" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# リージョンを設定
$env:AWS_DEFAULT_REGION = $Region

Write-Host "Backend URL: $BackendUrl" -ForegroundColor Gray
Write-Host ""

# CloudFrontディストリビューションを作成
Write-Host "CloudFrontディストリビューションを作成中..." -ForegroundColor Yellow

# Origin domainを抽出
$originDomain = $BackendUrl -replace '^https?://', ''

Write-Host "Origin domain: $originDomain" -ForegroundColor Gray

# CloudFrontディストリビューション設定のJSONを作成
$distributionConfig = @{
    CallerReference = "basic-info-study-app-$(Get-Date -Format 'yyyyMMddHHmmss')"
    Comment = "HTTPS access for Basic Info Study App API"
    Origins = @{
        Quantity = 1
        Items = @(
            @{
                Id = "basic-info-study-app-origin"
                DomainName = $originDomain
                CustomOriginConfig = @{
                    HTTPPort = 80
                    HTTPSPort = 443
                    OriginProtocolPolicy = "http-only"
                    OriginSslProtocols = @{
                        Quantity = 1
                        Items = @("TLSv1.2")
                    }
                }
            }
        )
    }
    DefaultCacheBehavior = @{
        TargetOriginId = "basic-info-study-app-origin"
        ViewerProtocolPolicy = "redirect-to-https"
        AllowedMethods = @{
            Quantity = 7
            Items = @("GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE")
            CachedMethods = @{
                Quantity = 2
                Items = @("GET", "HEAD")
            }
        }
        ForwardedValues = @{
            QueryString = $true
            Cookies = @{
                Forward = "all"
            }
            Headers = @{
                Quantity = 1
                Items = @("*")
            }
        }
        MinTTL = 0
        DefaultTTL = 0
        MaxTTL = 0
        Compress = $true
    }
    Enabled = $true
    PriceClass = "PriceClass_All"
} | ConvertTo-Json -Depth 10

# 一時ファイルに保存
$configFile = Join-Path $env:TEMP "cloudfront-config.json"
$distributionConfig | Out-File -FilePath $configFile -Encoding UTF8

try {
    Write-Host "CloudFrontディストリビューションを作成しています..." -ForegroundColor Yellow
    Write-Host "（この処理には5-15分かかります）" -ForegroundColor Gray
    
    $result = aws cloudfront create-distribution `
        --distribution-config "file://$configFile" `
        --region $Region `
        --output json 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "エラー: CloudFrontディストリビューションの作成に失敗しました" -ForegroundColor Red
        Write-Host $result -ForegroundColor Red
        exit 1
    }
    
    $distribution = $result | ConvertFrom-Json
    $distributionId = $distribution.Distribution.Id
    $domainName = $distribution.Distribution.DomainName
    
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "CloudFrontディストリビューション作成完了！" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Distribution ID: $distributionId" -ForegroundColor Cyan
    Write-Host "Domain Name: $domainName" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "次のステップ:" -ForegroundColor Yellow
    Write-Host "1. CloudFrontのデプロイを待つ（5-15分）" -ForegroundColor White
    Write-Host "   ステータス確認: aws cloudfront get-distribution --id $distributionId --query 'Distribution.Status' --output text" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Amplifyの環境変数を更新:" -ForegroundColor White
    Write-Host "   キー: VUE_APP_API_URL" -ForegroundColor Cyan
    Write-Host "   値: https://$domainName/api" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "3. Amplifyアプリを再デプロイ" -ForegroundColor White
    Write-Host ""
    Write-Host "CloudFrontコンソール:" -ForegroundColor Yellow
    Write-Host "https://console.aws.amazon.com/cloudfront/v3/home?region=ap-northeast-1#/distributions/$distributionId" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "エラー: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} finally {
    # 一時ファイルを削除
    if (Test-Path $configFile) {
        Remove-Item $configFile -Force -ErrorAction SilentlyContinue
    }
}

