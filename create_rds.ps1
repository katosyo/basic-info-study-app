# RDS PostgreSQLインスタンス作成スクリプト
# 使用方法: .\create_rds.ps1 -Password "your-strong-password"

param(
    [Parameter(Mandatory=$true)]
    [string]$Password,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "ap-northeast-1",
    
    [Parameter(Mandatory=$false)]
    [string]$DBInstanceIdentifier = "basic-info-study-db"
)

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "RDS PostgreSQL インスタンス作成スクリプト" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# リージョンを設定
$env:AWS_DEFAULT_REGION = $Region
Write-Host "リージョン: $Region" -ForegroundColor Green

# デフォルトVPCを取得
Write-Host "デフォルトVPCを取得中..." -ForegroundColor Yellow
try {
    $vpcId = aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text --region $Region
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($vpcId)) {
        Write-Host "エラー: デフォルトVPCが見つかりませんでした。" -ForegroundColor Red
        Write-Host "AWSコンソールでVPCを確認するか、手動でVPC IDを指定してください。" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "VPC ID: $vpcId" -ForegroundColor Green
} catch {
    Write-Host "エラー: VPCの取得に失敗しました: $_" -ForegroundColor Red
    exit 1
}

# サブネットグループ名を生成（既存のものがあれば使用）
$subnetGroupName = "default-vpc-subnet-group"

# デフォルトサブネットを取得
Write-Host "デフォルトサブネットを取得中..." -ForegroundColor Yellow
try {
    $subnets = aws ec2 describe-subnets --filters "Name=vpc-id,Values=$vpcId" --query "Subnets[*].SubnetId" --output text --region $Region
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($subnets)) {
        Write-Host "エラー: サブネットが見つかりませんでした。" -ForegroundColor Red
        exit 1
    }
    $subnetArray = $subnets -split "`t"
    Write-Host "サブネット数: $($subnetArray.Count)" -ForegroundColor Green
} catch {
    Write-Host "エラー: サブネットの取得に失敗しました: $_" -ForegroundColor Red
    exit 1
}

# サブネットグループが存在するか確認
Write-Host "サブネットグループを確認中..." -ForegroundColor Yellow
$existingGroup = aws rds describe-db-subnet-groups --db-subnet-group-name $subnetGroupName --region $Region 2>$null
if ($LASTEXITCODE -ne 0) {
    # サブネットグループが存在しない場合は作成
    Write-Host "サブネットグループを作成中..." -ForegroundColor Yellow
    $subnetGroupJson = @{
        DBSubnetGroupName = $subnetGroupName
        DBSubnetGroupDescription = "Default VPC subnet group for RDS"
        SubnetIds = $subnetArray
    } | ConvertTo-Json -Compress
    
    $subnetGroupJson = $subnetGroupJson -replace '"', '\"'
    aws rds create-db-subnet-group `
        --db-subnet-group-name $subnetGroupName `
        --db-subnet-group-description "Default VPC subnet group for RDS" `
        --subnet-ids $subnetArray `
        --region $Region
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "エラー: サブネットグループの作成に失敗しました。" -ForegroundColor Red
        exit 1
    }
    Write-Host "サブネットグループを作成しました: $subnetGroupName" -ForegroundColor Green
} else {
    Write-Host "サブネットグループは既に存在します: $subnetGroupName" -ForegroundColor Green
}

# セキュリティグループを作成
Write-Host "セキュリティグループを作成中..." -ForegroundColor Yellow
$securityGroupName = "rds-postgres-sg"
$securityGroupDescription = "Security group for RDS PostgreSQL instance"

# 既存のセキュリティグループを確認
$existingSG = aws ec2 describe-security-groups --filters "Name=group-name,Values=$securityGroupName" --query "SecurityGroups[0].GroupId" --output text --region $Region 2>$null
if ($LASTEXITCODE -eq 0 -and ![string]::IsNullOrWhiteSpace($existingSG) -and $existingSG -ne "None") {
    Write-Host "セキュリティグループは既に存在します: $existingSG" -ForegroundColor Green
    $securityGroupId = $existingSG
} else {
    $sgResult = aws ec2 create-security-group `
        --group-name $securityGroupName `
        --description $securityGroupDescription `
        --vpc-id $vpcId `
        --region $Region `
        --output json
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "エラー: セキュリティグループの作成に失敗しました。" -ForegroundColor Red
        exit 1
    }
    
    $sgJson = $sgResult | ConvertFrom-Json
    $securityGroupId = $sgJson.GroupId
    Write-Host "セキュリティグループを作成しました: $securityGroupId" -ForegroundColor Green
    
    # セキュリティグループにインバウンドルールを追加（後でElastic Beanstalkから接続できるように）
    # 一旦、同じVPC内からのアクセスのみ許可
    Write-Host "セキュリティグループのルールを設定中..." -ForegroundColor Yellow
    aws ec2 authorize-security-group-ingress `
        --group-id $securityGroupId `
        --protocol tcp `
        --port 5432 `
        --cidr $vpcId `
        --region $Region 2>$null
    
    # VPCのCIDRブロックを取得して設定
    $vpcCidr = aws ec2 describe-vpcs --vpc-ids $vpcId --query "Vpcs[0].CidrBlock" --output text --region $Region
    if ($LASTEXITCODE -eq 0 -and ![string]::IsNullOrWhiteSpace($vpcCidr)) {
        aws ec2 authorize-security-group-ingress `
            --group-id $securityGroupId `
            --protocol tcp `
            --port 5432 `
            --cidr $vpcCidr `
            --region $Region 2>$null
    }
}

# RDSインスタンスが既に存在するか確認
Write-Host "RDSインスタンスの存在を確認中..." -ForegroundColor Yellow
$existingDB = aws rds describe-db-instances --db-instance-identifier $DBInstanceIdentifier --region $Region 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "警告: RDSインスタンス '$DBInstanceIdentifier' は既に存在します。" -ForegroundColor Yellow
    Write-Host "既存のインスタンス情報を表示します..." -ForegroundColor Yellow
    aws rds describe-db-instances --db-instance-identifier $DBInstanceIdentifier --query "DBInstances[0].{Endpoint:Endpoint.Address,Port:Endpoint.Port,Status:DBInstanceStatus}" --region $Region --output table
    exit 0
}

# RDSインスタンスを作成
Write-Host "RDSインスタンスを作成中..." -ForegroundColor Yellow
Write-Host "インスタンス識別子: $DBInstanceIdentifier" -ForegroundColor Cyan
Write-Host "マスターユーザー名: postgres" -ForegroundColor Cyan
Write-Host "インスタンスクラス: db.t3.micro" -ForegroundColor Cyan
Write-Host ""

$createResult = aws rds create-db-instance `
    --db-instance-identifier $DBInstanceIdentifier `
    --db-instance-class db.t3.micro `
    --engine postgres `
    --engine-version 15.5 `
    --master-username postgres `
    --master-user-password $Password `
    --allocated-storage 20 `
    --storage-type gp3 `
    --db-name postgres `
    --vpc-security-group-ids $securityGroupId `
    --db-subnet-group-name $subnetGroupName `
    --backup-retention-period 7 `
    --no-publicly-accessible `
    --no-multi-az `
    --region $Region `
    --output json

if ($LASTEXITCODE -ne 0) {
    Write-Host "エラー: RDSインスタンスの作成に失敗しました。" -ForegroundColor Red
    Write-Host $createResult -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "RDSインスタンスの作成を開始しました！" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "作成には5-10分かかります。" -ForegroundColor Yellow
Write-Host "進行状況を確認するには以下を実行してください:" -ForegroundColor Yellow
Write-Host "  aws rds describe-db-instances --db-instance-identifier $DBInstanceIdentifier --query 'DBInstances[0].DBInstanceStatus' --region $Region" -ForegroundColor Cyan
Write-Host ""
Write-Host "エンドポイントを取得するには:" -ForegroundColor Yellow
Write-Host "  aws rds describe-db-instances --db-instance-identifier $DBInstanceIdentifier --query 'DBInstances[0].Endpoint.Address' --region $Region --output text" -ForegroundColor Cyan
Write-Host ""
Write-Host "重要: 以下の情報を記録してください:" -ForegroundColor Red
Write-Host "  - エンドポイント: (上記コマンドで取得)" -ForegroundColor White
Write-Host "  - ポート: 5432" -ForegroundColor White
Write-Host "  - データベース名: postgres" -ForegroundColor White
Write-Host "  - ユーザー名: postgres" -ForegroundColor White
Write-Host "  - パスワード: $Password" -ForegroundColor White
Write-Host "  - セキュリティグループID: $securityGroupId" -ForegroundColor White
Write-Host ""

