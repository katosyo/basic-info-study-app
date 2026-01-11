# PowerShellスクリプトで実行する場合
# Set-Location ".\backend"
$env:FLASK_APP="backend"
.\backend\venv\Scripts\activate.ps1
flask run --host=0.0.0.0 --port=8000
