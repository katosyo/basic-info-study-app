from . import create_app, db

app = create_app()

with app.app_context():
    # すべてのテーブルを削除
    db.drop_all()
    print("既存のテーブルを削除しました。")
    
    # すべてのテーブルを再作成
    db.create_all()
    print("データベースを再作成しました。")

