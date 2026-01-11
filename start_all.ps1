# 基本情報勉強アプリ - 一括起動スクリプト
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "基本情報勉強アプリ - 一括起動" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 現在のディレクトリを取得
$currentDir = Get-Location

# 既存のサーバープロセスを停止
Write-Host "既存のサーバープロセスを確認しています..." -ForegroundColor Yellow

# 関数: プロセスとその親プロセス（PowerShellウィンドウ）を停止
function Stop-ProcessWithParent {
    param($ProcessId)
    
    try {
        $process = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
        if ($process) {
            # プロセスを停止
            Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
            
            # 親プロセスを取得
            $parentId = (Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" | Select-Object -ExpandProperty ParentProcessId)
            if ($parentId) {
                $parentProcess = Get-Process -Id $parentId -ErrorAction SilentlyContinue
                if ($parentProcess -and $parentProcess.ProcessName -eq "powershell") {
                    # 親プロセスがPowerShellの場合、コマンドラインを確認
                    $commandLine = (Get-CimInstance Win32_Process -Filter "ProcessId = $parentId" | Select-Object -ExpandProperty CommandLine)
                    if ($commandLine -match "start_backend\.ps1|start_frontend\.ps1") {
                        Stop-Process -Id $parentId -Force -ErrorAction SilentlyContinue
                        return $true
                    }
                }
            }
            return $true
        }
    } catch {
        return $false
    }
    return $false
}

# ポート8000を使用しているプロセス（バックエンド）を停止
$backendProcesses = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($backendProcesses) {
    foreach ($processId in $backendProcesses) {
        if (Stop-ProcessWithParent -ProcessId $processId) {
            Write-Host "バックエンドプロセス (PID: $processId) とそのウィンドウを停止しました。" -ForegroundColor Green
        } else {
            Write-Host "バックエンドプロセス (PID: $processId) の停止に失敗しました。" -ForegroundColor Yellow
        }
    }
    Start-Sleep -Seconds 1
}

# ポート3000を使用しているプロセス（フロントエンド）を停止
$frontendProcesses = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($frontendProcesses) {
    foreach ($processId in $frontendProcesses) {
        if (Stop-ProcessWithParent -ProcessId $processId) {
            Write-Host "フロントエンドプロセス (PID: $processId) とそのウィンドウを停止しました。" -ForegroundColor Green
        } else {
            Write-Host "フロントエンドプロセス (PID: $processId) の停止に失敗しました。" -ForegroundColor Yellow
        }
    }
    Start-Sleep -Seconds 1
}

# start_backend.ps1やstart_frontend.ps1を実行しているPowerShellプロセスも直接検索して停止
$backendScriptPath = Join-Path $currentDir "start_backend.ps1"
$frontendScriptPath = Join-Path $currentDir "start_frontend.ps1"

$powershellProcesses = Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe'" | Where-Object {
    $_.CommandLine -match [regex]::Escape($backendScriptPath) -or $_.CommandLine -match [regex]::Escape($frontendScriptPath)
}

foreach ($proc in $powershellProcesses) {
    try {
        Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
        Write-Host "サーバー起動用PowerShellウィンドウ (PID: $($proc.ProcessId)) を停止しました。" -ForegroundColor Green
    } catch {
        # 既に停止している場合は無視
    }
}

if (-not $backendProcesses -and -not $frontendProcesses -and -not $powershellProcesses) {
    Write-Host "既存のサーバープロセスは見つかりませんでした。" -ForegroundColor Green
}

Write-Host ""

$dbPath = Join-Path $currentDir "instance\site.db"

$dbExists = Test-Path $dbPath
if ($dbExists -eq $false) {
    Write-Host "データベースが見つかりません。初期化を実行します..." -ForegroundColor Yellow
    python -m backend.create_db
    Write-Host "データベースの初期化が完了しました。" -ForegroundColor Green
    Write-Host "問題データを投入します..." -ForegroundColor Yellow
    python -m backend.seed_data
    Write-Host "問題データの投入が完了しました。" -ForegroundColor Green
}

Write-Host ""

Write-Host "バックエンドを起動しています..." -ForegroundColor Yellow
$backendScript = Join-Path $currentDir "start_backend.ps1"
Start-Process powershell -ArgumentList "-NoExit", "-File", "`"$backendScript`"" -WindowStyle Normal
Start-Sleep -Seconds 2
Write-Host "バックエンドが起動しました。 http://127.0.0.1:8000" -ForegroundColor Green

Write-Host "フロントエンドを起動しています..." -ForegroundColor Yellow
$frontendScript = Join-Path $currentDir "start_frontend.ps1"
Start-Process powershell -ArgumentList "-NoExit", "-File", "`"$frontendScript`"" -WindowStyle Normal
Start-Sleep -Seconds 2
Write-Host "フロントエンドが起動しました。 http://localhost:3000" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "起動完了！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "バックエンド: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "フロントエンド: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Close each window to stop the application." -ForegroundColor Yellow
Write-Host ""
