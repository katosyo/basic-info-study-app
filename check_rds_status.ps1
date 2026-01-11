# RDS Instance Status Check Script

param(
    [Parameter(Mandatory=$false)]
    [string]$DBInstanceIdentifier = "basic-info-study-db",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "ap-northeast-1"
)

$env:AWS_DEFAULT_REGION = $Region

Write-Host "Checking RDS instance status..." -ForegroundColor Yellow
Write-Host ""

$status = aws rds describe-db-instances --db-instance-identifier $DBInstanceIdentifier --query "DBInstances[0].DBInstanceStatus" --region $Region --output text 2>$null

if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($status)) {
    Write-Host "Error: RDS instance '$DBInstanceIdentifier' not found." -ForegroundColor Red
    exit 1
}

Write-Host "Status: $status" -ForegroundColor $(if ($status -eq "available") { "Green" } else { "Yellow" })
Write-Host ""

if ($status -eq "available") {
    $endpoint = aws rds describe-db-instances --db-instance-identifier $DBInstanceIdentifier --query "DBInstances[0].Endpoint.Address" --region $Region --output text
    $port = aws rds describe-db-instances --db-instance-identifier $DBInstanceIdentifier --query "DBInstances[0].Endpoint.Port" --region $Region --output text
    
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "RDS instance is available!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Connection Info:" -ForegroundColor Cyan
    Write-Host "  Endpoint: $endpoint" -ForegroundColor White
    Write-Host "  Port: $port" -ForegroundColor White
    Write-Host "  Database: postgres" -ForegroundColor White
    Write-Host "  Username: postgres" -ForegroundColor White
    Write-Host ""
    Write-Host "DATABASE_URL format:" -ForegroundColor Cyan
    $databaseUrl = "postgresql://postgres:PASSWORD@${endpoint}:${port}/postgres"
    Write-Host "  $databaseUrl" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "RDS instance is still being created. Please wait and try again later." -ForegroundColor Yellow
}
