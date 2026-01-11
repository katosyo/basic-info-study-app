from . import create_app, db
from .models import Question, Option
from .question_data import QUESTIONS_DATA, generate_questions_to_500

app = create_app()

with app.app_context():
    # 既存の問題データを全て削除 (開発時のみ)
    db.session.query(Option).delete()
    db.session.query(Question).delete()
    db.session.commit()

    # 500問を生成
    questions_data = generate_questions_to_500()
    
    print(f"問題データを生成しました。合計{len(questions_data)}問。")
    print("データベースに投入中...")

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
            print(f"進捗: {idx + 1}/{len(questions_data)}問を投入しました。")

    print(f"問題データをデータベースに投入しました。合計{len(questions_data)}問。")
