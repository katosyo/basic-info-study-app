# Simple RDS Creation Script (without free tier dependency)
# Usage: .\create_rds_simple.ps1 -Password "your-password"

param(
    [Parameter(Mandatory=$true)]
    [string]$Password,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "ap-northeast-1",
    
    [Parameter(Mandatory=$false)]
    [string]$DBInstanceIdentifier = "basic-info-study-db"
)

$ErrorActionPreference = "Continue"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Creating RDS PostgreSQL Instance" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Set region
$env:AWS_DEFAULT_REGION = $Region
Write-Host "Region: $Region" -ForegroundColor Green

# Get default VPC
Write-Host "Getting default VPC..." -ForegroundColor Yellow
$vpcId = aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text --region $Region 2>&1
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($vpcId) -or $vpcId -eq "None") {
    Write-Host "Error: Default VPC not found" -ForegroundColor Red
    Write-Host $vpcId -ForegroundColor Red
    exit 1
}
Write-Host "VPC ID: $vpcId" -ForegroundColor Green

# Get subnets
Write-Host "Getting subnets..." -ForegroundColor Yellow
$subnets = aws ec2 describe-subnets --filters "Name=vpc-id,Values=$vpcId" --query "Subnets[*].SubnetId" --output text --region $Region 2>&1
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($subnets)) {
    Write-Host "Error: Subnets not found" -ForegroundColor Red
    Write-Host $subnets -ForegroundColor Red
    exit 1
}
$subnetArray = $subnets -split "`t" | Where-Object { $_ -ne "" }
Write-Host "Found $($subnetArray.Count) subnets: $($subnetArray -join ', ')" -ForegroundColor Green

# Create or use subnet group
$subnetGroupName = "default-vpc-subnet-group"
Write-Host "Checking subnet group..." -ForegroundColor Yellow
$existingGroup = aws rds describe-db-subnet-groups --db-subnet-group-name $subnetGroupName --region $Region 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Subnet group does not exist. Creating..." -ForegroundColor Yellow
    $createGroupResult = aws rds create-db-subnet-group `
        --db-subnet-group-name $subnetGroupName `
        --db-subnet-group-description "Default VPC subnet group" `
        --subnet-ids $subnetArray `
        --region $Region 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create subnet group" -ForegroundColor Red
        Write-Host $createGroupResult -ForegroundColor Red
        exit 1
    }
    Write-Host "Subnet group created: $subnetGroupName" -ForegroundColor Green
} else {
    Write-Host "Subnet group exists: $subnetGroupName" -ForegroundColor Green
}

# Create security group
Write-Host "Creating security group..." -ForegroundColor Yellow
$securityGroupName = "rds-postgres-sg"
$existingSG = aws ec2 describe-security-groups --filters "Name=group-name,Values=$securityGroupName" "Name=vpc-id,Values=$vpcId" --query "SecurityGroups[0].GroupId" --output text --region $Region 2>&1
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($existingSG) -or $existingSG -eq "None") {
    Write-Host "Security group does not exist. Creating..." -ForegroundColor Yellow
    $sgResult = aws ec2 create-security-group `
        --group-name $securityGroupName `
        --description "Security group for RDS PostgreSQL" `
        --vpc-id $vpcId `
        --region $Region `
        --output json 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create security group" -ForegroundColor Red
        Write-Host $sgResult -ForegroundColor Red
        exit 1
    }
    
    $sgJson = $sgResult | ConvertFrom-Json
    $securityGroupId = $sgJson.GroupId
    Write-Host "Security group created: $securityGroupId" -ForegroundColor Green
    
    # Get VPC CIDR and add ingress rule
    $vpcCidr = aws ec2 describe-vpcs --vpc-ids $vpcId --query "Vpcs[0].CidrBlock" --output text --region $Region 2>&1
    if ($LASTEXITCODE -eq 0 -and ![string]::IsNullOrWhiteSpace($vpcCidr) -and $vpcCidr -ne "None") {
        Write-Host "Adding ingress rule for VPC CIDR: $vpcCidr" -ForegroundColor Yellow
        $ingressResult = aws ec2 authorize-security-group-ingress `
            --group-id $securityGroupId `
            --protocol tcp `
            --port 5432 `
            --cidr $vpcCidr `
            --region $Region 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Warning: Failed to add ingress rule (may already exist): $ingressResult" -ForegroundColor Yellow
        }
    }
} else {
    $securityGroupId = $existingSG
    Write-Host "Security group exists: $securityGroupId" -ForegroundColor Green
}

# Check if RDS instance already exists
Write-Host "Checking if RDS instance exists..." -ForegroundColor Yellow
$existingDB = aws rds describe-db-instances --db-instance-identifier $DBInstanceIdentifier --region $Region 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Warning: RDS instance '$DBInstanceIdentifier' already exists" -ForegroundColor Yellow
    Write-Host "Getting instance info..." -ForegroundColor Yellow
    aws rds describe-db-instances --db-instance-identifier $DBInstanceIdentifier --query "DBInstances[0].{Endpoint:Endpoint.Address,Port:Endpoint.Port,Status:DBInstanceStatus}" --region $Region --output table
    exit 0
}

# Create RDS instance
Write-Host ""
Write-Host "Creating RDS instance..." -ForegroundColor Yellow
Write-Host "Instance ID: $DBInstanceIdentifier" -ForegroundColor Cyan
Write-Host "Master username: postgres" -ForegroundColor Cyan
Write-Host "Instance class: db.t3.micro" -ForegroundColor Cyan
Write-Host ""

$createResult = aws rds create-db-instance `
    --db-instance-identifier $DBInstanceIdentifier `
    --db-instance-class db.t3.micro `
    --engine postgres `
    --engine-version 15.15 `
    --master-username postgres `
    --master-user-password $Password `
    --allocated-storage 20 `
    --storage-type gp3 `
    --db-name postgres `
    --vpc-security-group-ids $securityGroupId `
    --db-subnet-group-name $subnetGroupName `
    --backup-retention-period 0 `
    --no-publicly-accessible `
    --no-multi-az `
    --region $Region `
    --output json

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to create RDS instance" -ForegroundColor Red
    Write-Host $createResult -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "RDS instance creation started!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "This will take 5-10 minutes." -ForegroundColor Yellow
Write-Host ""
Write-Host "To check status, run:" -ForegroundColor Yellow
Write-Host "  .\check_rds_status.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Important: Record these details:" -ForegroundColor Red
Write-Host "  - Endpoint: (run check script to get)" -ForegroundColor White
Write-Host "  - Port: 5432" -ForegroundColor White
Write-Host "  - Database: postgres" -ForegroundColor White
Write-Host "  - Username: postgres" -ForegroundColor White
Write-Host "  - Password: $Password" -ForegroundColor White
Write-Host "  - Security Group ID: $securityGroupId" -ForegroundColor White
Write-Host ""

