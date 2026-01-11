from flask import Blueprint, request, jsonify
from ..services.question_service import QuestionService
# from flask_login import login_required, current_user # ログイン中のユーザー情報を取得するために必要

questions_bp = Blueprint('questions', __name__)

@questions_bp.route('/random', methods=['GET'])
# @login_required # 後で導入
def get_random_question():
    question = QuestionService.get_random_question()
    if question:
        options = [{'id': opt.id, 'option_text': opt.option_text, 'is_correct': opt.is_correct} for opt in question.options]
        return jsonify({
            'id': question.id,
            'question_text': question.question_text,
            'question_type': question.question_type,
            'category': question.category,
            'difficulty': question.difficulty,
            'explanation': question.explanation,
            'options': options
        }), 200
    return jsonify({'message': 'No questions found'}), 404

@questions_bp.route('/submit_answer', methods=['POST'])
# @login_required # 後で導入
def submit_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    selected_option_id = data.get('selected_option_id')
    user_id = data.get('user_id')

    if not question_id or not selected_option_id:
        return jsonify({'message': 'Missing question_id or selected_option_id'}), 400

    # user_idが提供されている場合のみ解答を保存
    if user_id:
        try:
            is_correct = QuestionService.submit_answer(user_id, question_id, selected_option_id)
            return jsonify({'is_correct': is_correct}), 200
        except ValueError as e:
            return jsonify({'message': str(e)}), 400
        except Exception as e:
            return jsonify({'message': 'Internal Server Error'}), 500
    else:
        # user_idがない場合は、正誤判定のみを返す（保存しない）
        try:
            question = QuestionService.get_question_by_id(question_id)
            if not question:
                return jsonify({'message': 'Question not found'}), 404
            
            selected_option = None
            for opt in question.options:
                if opt.id == selected_option_id:
                    selected_option = opt
                    break
            
            if not selected_option or selected_option.question_id != question_id:
                return jsonify({'message': 'Invalid option for this question'}), 400
            
            is_correct = selected_option.is_correct
            return jsonify({'is_correct': is_correct}), 200
        except Exception as e:
            return jsonify({'message': 'Internal Server Error'}), 500

@questions_bp.route('/categories', methods=['GET'])
def get_categories():
    """ジャンル一覧を取得"""
    categories = QuestionService.get_categories()
    return jsonify({'categories': categories}), 200

@questions_bp.route('/by_criteria', methods=['POST'])
def get_questions_by_criteria():
    """条件に基づいて問題を取得"""
    data = request.get_json()
    categories = data.get('categories', [])
    count = data.get('count', 10)
    order = data.get('order', 'random')  # 'random', 'unseen', 'incorrect'
    user_id = data.get('user_id')  # オプショナル
    
    # 空のリストの場合はNoneを渡す（すべてのカテゴリを取得）
    categories_param = categories if categories and len(categories) > 0 else None
    
    questions = QuestionService.get_questions_by_criteria(
        categories=categories_param,
        count=count,
        order=order,
        user_id=user_id
    )
    
    if not questions:
        return jsonify({'message': 'No questions found'}), 404
    
    result = []
    for question in questions:
        options = [{'id': opt.id, 'option_text': opt.option_text, 'is_correct': opt.is_correct} for opt in question.options]
        result.append({
            'id': question.id,
            'question_text': question.question_text,
            'question_type': question.question_type,
            'category': question.category,
            'difficulty': question.difficulty,
            'explanation': question.explanation,
            'options': options
        })
    
    return jsonify({'questions': result}), 200

@questions_bp.route('/submit_answers', methods=['POST'])
def submit_answers():
    """複数の解答を一括で送信"""
    data = request.get_json()
    answers = data.get('answers', [])
    user_id = data.get('user_id')
    
    if not answers:
        return jsonify({'message': 'Missing answers'}), 400
    
    # user_idが提供されている場合のみ解答を保存
    if user_id:
        try:
            results = QuestionService.submit_answers(user_id, answers)
            return jsonify({'results': results}), 200
        except Exception as e:
            return jsonify({'message': 'Internal Server Error'}), 500
    else:
        # user_idがない場合は、正誤判定のみを返す（保存しない）
        results = []
        for answer in answers:
            question_id = answer.get('question_id')
            selected_option_id = answer.get('selected_option_id')
            
            if not question_id or not selected_option_id:
                continue
            
            try:
                question = QuestionService.get_question_by_id(question_id)
                if question:
                    selected_option = None
                    for opt in question.options:
                        if opt.id == selected_option_id:
                            selected_option = opt
                            break
                    
                    if selected_option:
                        is_correct = selected_option.is_correct
                        results.append({
                            'question_id': question_id,
                            'is_correct': is_correct
                        })
            except Exception:
                results.append({
                    'question_id': question_id,
                    'is_correct': False,
                    'error': 'Invalid answer'
                })
        
        return jsonify({'results': results}), 200

@questions_bp.route('/answer_history/<int:user_id>', methods=['GET'])
def get_answer_history(user_id):
    """ユーザーの解答履歴を取得"""
    try:
        print(f"解答履歴を取得します。ユーザーID: {user_id}")
        history = QuestionService.get_answer_history(user_id)
        print(f"取得した解答履歴の数: {len(history)}")
        return jsonify({'history': history}), 200
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"解答履歴取得エラー: {str(e)}")
        print(f"エラートレース: {error_trace}")
        return jsonify({'message': str(e)}), 500

@questions_bp.route('/incorrect_questions', methods=['POST'])
def get_incorrect_questions():
    """指定期間内の間違えた問題を取得"""
    data = request.get_json()
    user_id = data.get('user_id')
    period = data.get('period', 'all')  # '1hour', '1day', '1week', '2weeks', '1month', 'all'
    
    if not user_id:
        return jsonify({'message': 'Missing user_id'}), 400
    
    try:
        questions = QuestionService.get_incorrect_questions(user_id, period)
        return jsonify({'questions': questions}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@questions_bp.route('/statistics/<int:user_id>', methods=['GET'])
def get_user_statistics(user_id):
    """ユーザーの学習統計情報を取得"""
    try:
        statistics = QuestionService.get_user_statistics(user_id)
        return jsonify(statistics), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question_by_id(question_id):
    """問題IDで問題を取得"""
    question = QuestionService.get_question_by_id(question_id)
    if question:
        options = [{'id': opt.id, 'option_text': opt.option_text, 'is_correct': opt.is_correct} for opt in question.options]
        return jsonify({
            'id': question.id,
            'question_text': question.question_text,
            'question_type': question.question_type,
            'category': question.category,
            'difficulty': question.difficulty,
            'explanation': question.explanation,
            'options': options
        }), 200
    return jsonify({'message': 'Question not found'}), 404

