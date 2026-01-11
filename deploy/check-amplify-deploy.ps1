# Amplifyデプロイ状況確認スクリプト

param(
    [Parameter(Mandatory=$false)]
    [string]$AppId = "dlnofxx6dv6xm",
    
    [Parameter(Mandatory=$false)]
    [string]$BranchName = "main",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "ap-northeast-1"
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Amplify Deploy Status Check" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# リージョンを設定
$env:AWS_DEFAULT_REGION = $Region

Write-Host "App ID: $AppId" -ForegroundColor Gray
Write-Host "Branch: $BranchName" -ForegroundColor Gray
Write-Host ""

# 最新のデプロイジョブを取得
Write-Host "最新のデプロイジョブを確認中..." -ForegroundColor Yellow

$jobs = aws amplify list-jobs `
    --app-id $AppId `
    --branch-name $BranchName `
    --region $Region `
    --max-results 5 `
    --output json 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "エラー: デプロイジョブの取得に失敗しました" -ForegroundColor Red
    Write-Host $jobs -ForegroundColor Red
    exit 1
}

$jobsJson = $jobs | ConvertFrom-Json

if ($jobsJson.jobSummaries.Count -eq 0) {
    Write-Host "デプロイジョブが見つかりませんでした。" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Amplifyコンソールで確認してください:" -ForegroundColor Cyan
    Write-Host "https://ap-northeast-1.console.aws.amazon.com/amplify/home?region=ap-northeast-1#/$AppId" -ForegroundColor White
    exit 0
}

Write-Host ""
Write-Host "デプロイジョブ一覧:" -ForegroundColor Green
Write-Host ""

foreach ($job in $jobsJson.jobSummaries) {
    $statusColor = switch ($job.status) {
        "SUCCEED" { "Green" }
        "FAILED" { "Red" }
        "PENDING" { "Yellow" }
        "RUNNING" { "Cyan" }
        default { "Gray" }
    }
    
    Write-Host "  Job ID: $($job.jobId)" -ForegroundColor White
    Write-Host "  ステータス: $($job.status)" -ForegroundColor $statusColor
    Write-Host "  開始時刻: $($job.startTime)" -ForegroundColor Gray
    
    if ($job.endTime) {
        Write-Host "  終了時刻: $($job.endTime)" -ForegroundColor Gray
    }
    
    Write-Host ""
}

# 最新のジョブの詳細を取得
$latestJob = $jobsJson.jobSummaries[0]
Write-Host "最新のデプロイジョブの詳細を取得中..." -ForegroundColor Yellow

$jobDetail = aws amplify get-job `
    --app-id $AppId `
    --branch-name $BranchName `
    --job-id $latestJob.jobId `
    --region $Region `
    --output json 2>&1

if ($LASTEXITCODE -eq 0) {
    $jobDetailJson = $jobDetail | ConvertFrom-Json
    $job = $jobDetailJson.job
    
    Write-Host ""
    Write-Host "詳細情報:" -ForegroundColor Green
    Write-Host "  ステップ: $($job.steps.Count) ステップ" -ForegroundColor White
    
    if ($job.steps) {
        Write-Host ""
        Write-Host "  ステップ詳細:" -ForegroundColor Cyan
        foreach ($step in $job.steps) {
            $stepStatusColor = switch ($step.status) {
                "SUCCESS" { "Green" }
                "FAILURE" { "Red" }
                "PENDING" { "Yellow" }
                "RUNNING" { "Cyan" }
                default { "Gray" }
            }
            
            Write-Host "    - $($step.stepName): $($step.status)" -ForegroundColor $stepStatusColor
            
            if ($step.logUrl) {
                Write-Host "      ログ: $($step.logUrl)" -ForegroundColor Gray
            }
        }
    }
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "確認完了" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Amplifyコンソール:" -ForegroundColor Cyan
Write-Host "https://ap-northeast-1.console.aws.amazon.com/amplify/home?region=ap-northeast-1#/$AppId" -ForegroundColor White
Write-Host ""
Write-Host "フロントエンドURL:" -ForegroundColor Cyan
Write-Host "https://main.dlnofxx6dv6xm.amplifyapp.com" -ForegroundColor White
Write-Host ""

