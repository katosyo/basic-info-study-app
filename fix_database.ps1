# データベース修正スクリプト（シンプル版）
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "データベース修正スクリプト" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 現在のディレクトリを取得
$currentDir = Get-Location

# instanceディレクトリが存在しない場合は作成
$instanceDir = Join-Path $currentDir "instance"
if (-not (Test-Path $instanceDir)) {
    New-Item -ItemType Directory -Path $instanceDir | Out-Null
    Write-Host "instanceディレクトリを作成しました。" -ForegroundColor Green
}

# データベースファイルのパス
$dbPath = Join-Path $instanceDir "site.db"

# データベースファイルが存在する場合は削除
if (Test-Path $dbPath) {
    Write-Host "既存のデータベースを削除しています..." -ForegroundColor Yellow
    Remove-Item $dbPath -Force
    Write-Host "データベースを削除しました。" -ForegroundColor Green
}

Write-Host ""
Write-Host "データベースを再作成しています..." -ForegroundColor Yellow

# 既存のスクリプトを使用
Set-Location $currentDir
python -c "from backend import create_app, db; from backend.models import Question, Option, User, UserAnswer; app = create_app(); app.app_context().push(); db.drop_all(); db.create_all(); print('データベースを再作成しました。')"

if ($LASTEXITCODE -eq 0) {
    Write-Host "データベースの再作成が完了しました。" -ForegroundColor Green
} else {
    Write-Host "データベースの再作成に失敗しました。" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "問題データを投入しています..." -ForegroundColor Yellow

python -c "from backend import create_app, db; from backend.models import Question, Option; from backend.question_data import generate_questions_to_500; app = create_app(); app.app_context().push(); db.session.query(Option).delete(); db.session.query(Question).delete(); db.session.commit(); questions_data = generate_questions_to_500(); print(f'問題データを生成しました。合計{len(questions_data)}問。'); print('データベースに投入中...'); [System.Linq.Enumerable]::Range(0, len(questions_data)).ToList() | ForEach-Object { idx = \$_; q_data = questions_data[idx]; options_data = q_data.pop('options'); explanation = q_data.pop('explanation', None); question = Question(question_text=q_data['question_text'], question_type=q_data.get('question_type', 'multiple_choice'), category=q_data['category'], difficulty=q_data['difficulty'], explanation=explanation); db.session.add(question); db.session.commit(); correct_option = None; [opt_data for opt_data in options_data].forEach(lambda opt_data: (option = Option(question_id=question.id, option_text=opt_data['option_text'], is_correct=opt_data['is_correct']); db.session.add(option); correct_option = option if opt_data['is_correct'] else correct_option)); question.correct_option_id = correct_option.id if correct_option else None; db.session.commit(); print(f'進捗: {idx + 1}/{len(questions_data)}問を投入しました。') if (idx + 1) % 50 == 0 else None }; print(f'問題データをデータベースに投入しました。合計{len(questions_data)}問。')"

# より簡単な方法：seed_data.pyを直接実行
python -m backend.seed_data

if ($LASTEXITCODE -eq 0) {
    Write-Host "問題データの投入が完了しました。" -ForegroundColor Green
} else {
    Write-Host "問題データの投入に失敗しました。" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "データベース修正完了！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "これで古い問題は削除され、最新の問題データが投入されました。" -ForegroundColor Green
Write-Host ""

