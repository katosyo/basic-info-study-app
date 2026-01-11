"""
管理用エンドポイント（本番環境では削除または認証を追加）
"""
from flask import Blueprint, jsonify
from backend import db
from backend.models import Question, Option
from backend.question_data import QUESTIONS_DATA, generate_questions_to_500

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/init-db', methods=['POST'])
def init_db():
    """データベースを初期化する（本番環境では認証を追加）"""
    try:
        with db.session.begin():
            # 既存データを削除
            db.session.query(Option).delete()
            db.session.query(Question).delete()
            
            # 500問を生成
            questions_data = generate_questions_to_500()
            
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
                db.session.flush()  # question_id を取得するためにflush
                
                correct_option = None
                for opt_data in options_data:
                    option = Option(question_id=question.id, option_text=opt_data['option_text'], is_correct=opt_data['is_correct'])
                    db.session.add(option)
                    if opt_data['is_correct']:
                        correct_option = option
                
                if correct_option:
                    question.correct_option_id = correct_option.id
            
        return jsonify({
            'status': 'success',
            'message': f'データベースを初期化しました。{len(questions_data)}問を投入しました。'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@admin_bp.route('/create-tables', methods=['POST'])
def create_tables():
    """データベーステーブルを作成する"""
    try:
        db.create_all()
        return jsonify({
            'status': 'success',
            'message': 'データベーステーブルを作成しました。'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

