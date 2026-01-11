# データベース再作成スクリプト
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "データベース再作成スクリプト" -ForegroundColor Cyan
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
} else {
    Write-Host "データベースファイルが見つかりませんでした。" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "データベースを再作成しています..." -ForegroundColor Yellow

# 一時的なPythonスクリプトファイルを作成
$tempRecreateScript = Join-Path $env:TEMP "recreate_db_temp.py"
$recreateScriptContent = @'
from backend import create_app, db
from backend.models import Question, Option, User, UserAnswer

app = create_app()

with app.app_context():
    # すべてのテーブルを削除
    db.drop_all()
    print('既存のテーブルを削除しました。')
    
    # すべてのテーブルを再作成
    db.create_all()
    print('データベースを再作成しました。')
'@

$recreateScriptContent | Out-File -FilePath $tempRecreateScript -Encoding UTF8
python $tempRecreateScript
if ($LASTEXITCODE -eq 0) {
    Write-Host "データベースの再作成が完了しました。" -ForegroundColor Green
} else {
    Write-Host "データベースの再作成に失敗しました。" -ForegroundColor Red
    Remove-Item $tempRecreateScript -ErrorAction SilentlyContinue
    exit 1
}
Remove-Item $tempRecreateScript -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "問題データを投入しています..." -ForegroundColor Yellow

# 一時的なPythonスクリプトファイルを作成
$tempSeedScript = Join-Path $env:TEMP "seed_data_temp.py"
$seedScriptContent = @'
from backend import create_app, db
from backend.models import Question, Option
from backend.question_data import QUESTIONS_DATA, generate_questions_to_500

app = create_app()

with app.app_context():
    # 既存の問題データを全て削除 (開発時のみ)
    db.session.query(Option).delete()
    db.session.query(Question).delete()
    db.session.commit()

    # 500問を生成
    questions_data = generate_questions_to_500()
    
    print(f'問題データを生成しました。合計{len(questions_data)}問。')
    print('データベースに投入中...')

    # 問題データをデータベースに投入
    for idx, q_data in enumerate(questions_data):
        options_data = q_data.pop('options')
        explanation = q_data.pop('explanation', None)
        question = Question(
            question_text=q_data['question_text'], 
            question_type=q_data.get('question_type', 'multiple_choice'), 
            category=q_data['category'], 
            difficulty=q_data['difficulty'],
            explanation=explanation
        )
        db.session.add(question)
        db.session.commit() # question_id を取得するために一旦コミット

        correct_option = None
        for opt_data in options_data:
            option = Option(question_id=question.id, option_text=opt_data['option_text'], is_correct=opt_data['is_correct'])
            db.session.add(option)
            if opt_data['is_correct']:
                correct_option = option
        
        if correct_option:
            question.correct_option_id = correct_option.id

        db.session.commit()
        
        if (idx + 1) % 50 == 0:
            print(f'進捗: {idx + 1}/{len(questions_data)}問を投入しました。')

    print(f'問題データをデータベースに投入しました。合計{len(questions_data)}問。')
'@

$seedScriptContent | Out-File -FilePath $tempSeedScript -Encoding UTF8
python $tempSeedScript
if ($LASTEXITCODE -eq 0) {
    Write-Host "問題データの投入が完了しました。" -ForegroundColor Green
} else {
    Write-Host "問題データの投入に失敗しました。" -ForegroundColor Red
    Remove-Item $tempSeedScript -ErrorAction SilentlyContinue
    exit 1
}
Remove-Item $tempSeedScript -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "データベース再作成完了！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "これで古い問題は削除され、最新の問題データが投入されました。" -ForegroundColor Green
Write-Host ""

