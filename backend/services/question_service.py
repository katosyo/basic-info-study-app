from .. import db
from ..models import Question, Option, UserAnswer
from datetime import datetime, timedelta, date
import random

class QuestionService:
    @staticmethod
    def get_random_question():
        questions = Question.query.all()
        if not questions:
            return None
        return random.choice(questions)
    
    @staticmethod
    def get_question_by_id(question_id):
        return Question.query.get(question_id)

    @staticmethod
    def submit_answer(user_id, question_id, selected_option_id):
        question = Question.query.get(question_id)
        if not question:
            raise ValueError('Question not found')

        selected_option = Option.query.get(selected_option_id)
        if not selected_option or selected_option.question_id != question_id:
            raise ValueError('Invalid option for this question')

        is_correct = selected_option.is_correct

        user_answer = UserAnswer(
            user_id=user_id,
            question_id=question_id,
            selected_option_id=selected_option_id,
            is_correct=is_correct
        )
        db.session.add(user_answer)
        db.session.commit()

        return is_correct

    @staticmethod
    def get_categories():
        """すべてのジャンル（カテゴリ）を取得"""
        categories = db.session.query(Question.category).distinct().all()
        return [cat[0] for cat in categories]
    
    @staticmethod
    def get_questions_by_criteria(categories=None, count=10, order='random', user_id=None):
        """
        条件に基づいて問題を取得
        
        Args:
            categories: ジャンルのリスト（Noneの場合はすべて）
            count: 取得する問題数
            order: 出題順（'random', 'unseen', 'incorrect'）
            user_id: ユーザーID（出題順に使用）
        """
        query = Question.query
        
        # ジャンルでフィルタ
        if categories and len(categories) > 0:
            query = query.filter(Question.category.in_(categories))
        
        all_questions = query.all()
        
        # 出題順に応じてソート
        if order == 'unseen' and user_id:
            # 見たことない問題優先
            answered_ids = set()
            answered_results = db.session.query(UserAnswer.question_id).filter(
                UserAnswer.user_id == user_id
            ).distinct().all()
            answered_ids = {qid[0] for qid in answered_results}
            unseen_questions = [q for q in all_questions if q.id not in answered_ids]
            seen_questions = [q for q in all_questions if q.id in answered_ids]
            questions = unseen_questions + seen_questions
        elif order == 'incorrect' and user_id:
            # 間違えた問題優先
            incorrect_results = db.session.query(UserAnswer.question_id).filter(
                UserAnswer.user_id == user_id,
                UserAnswer.is_correct == False
            ).distinct().all()
            incorrect_ids = {qid[0] for qid in incorrect_results}
            incorrect_questions = [q for q in all_questions if q.id in incorrect_ids]
            other_questions = [q for q in all_questions if q.id not in incorrect_ids]
            questions = incorrect_questions + other_questions
        else:
            # ランダム
            questions = all_questions.copy()
            random.shuffle(questions)
        
        # 指定された問題数を返す
        return questions[:count]
    
    @staticmethod
    def submit_answers(user_id, answers):
        """
        複数の解答を一括で送信
        
        Args:
            user_id: ユーザーID
            answers: 解答のリスト [{'question_id': int, 'selected_option_id': int}, ...]
        """
        results = []
        for answer in answers:
            question_id = answer.get('question_id')
            selected_option_id = answer.get('selected_option_id')
            
            if not question_id or not selected_option_id:
                continue
            
            try:
                is_correct = QuestionService.submit_answer(user_id, question_id, selected_option_id)
                results.append({
                    'question_id': question_id,
                    'is_correct': is_correct
                })
            except ValueError:
                results.append({
                    'question_id': question_id,
                    'is_correct': False,
                    'error': 'Invalid answer'
                })
        
        return results
    
    @staticmethod
    def get_answer_history(user_id):
        """ユーザーの解答履歴を取得（各問題の最新の解答のみ）"""
        try:
            # すべての解答を取得
            all_answers = UserAnswer.query.filter_by(user_id=user_id).order_by(UserAnswer.timestamp.desc()).all()
            
            # 各問題IDごとの最新の解答のみを保持
            seen_question_ids = set()
            latest_answers = []
            
            for answer in all_answers:
                if answer.question_id not in seen_question_ids:
                    seen_question_ids.add(answer.question_id)
                    latest_answers.append(answer)
            
            history = []
            for answer in latest_answers:
                question = Question.query.get(answer.question_id)
                if question:
                    # 同じ問題に対する解答回数を計算
                    same_question_answers = UserAnswer.query.filter_by(
                        user_id=user_id,
                        question_id=answer.question_id
                    ).all()
                    correct_count = sum(1 for a in same_question_answers if a.is_correct)
                    total_count = len(same_question_answers)
                    accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
                    
                    history.append({
                        'question_id': answer.question_id,
                        'question_text': question.question_text,
                        'category': question.category,
                        'is_correct': answer.is_correct,
                        'timestamp': answer.timestamp.isoformat(),
                        'accuracy': round(accuracy, 1),
                        'total_attempts': total_count,
                        'correct_attempts': correct_count
                    })
            
            # タイムスタンプでソート（新しい順）
            history.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return history
        except Exception as e:
            print(f"Error in get_answer_history: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    @staticmethod
    def get_incorrect_questions(user_id, period='all'):
        """指定期間内の間違えた問題を取得"""
        now = datetime.utcnow()
        
        # 期間に応じて開始時刻を設定
        if period == '1hour':
            start_time = now - timedelta(hours=1)
        elif period == '1day':
            start_time = now - timedelta(days=1)
        elif period == '1week':
            start_time = now - timedelta(weeks=1)
        elif period == '2weeks':
            start_time = now - timedelta(weeks=2)
        elif period == '1month':
            start_time = now - timedelta(days=30)
        else:  # 'all'
            start_time = None
        
        # 間違えた解答を取得
        query = UserAnswer.query.filter_by(
            user_id=user_id,
            is_correct=False
        )
        
        if start_time:
            query = query.filter(UserAnswer.timestamp >= start_time)
        
        incorrect_answers = query.all()
        
        # 問題IDのセットを作成（重複を排除）
        question_ids = set(answer.question_id for answer in incorrect_answers)
        
        # 問題を取得
        questions = []
        for question_id in question_ids:
            question = Question.query.get(question_id)
            if question:
                # この問題に対する間違えた回数をカウント
                incorrect_count = sum(1 for a in incorrect_answers if a.question_id == question_id)
                # この問題に対する全解答回数をカウント
                all_answers = UserAnswer.query.filter_by(
                    user_id=user_id,
                    question_id=question_id
                ).all()
                total_count = len(all_answers)
                correct_count = sum(1 for a in all_answers if a.is_correct)
                accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
                
                options = [{'id': opt.id, 'option_text': opt.option_text, 'is_correct': opt.is_correct} for opt in question.options]
                
                questions.append({
                    'id': question.id,
                    'question_text': question.question_text,
                    'question_type': question.question_type,
                    'category': question.category,
                    'difficulty': question.difficulty,
                    'explanation': question.explanation,
                    'options': options,
                    'incorrect_count': incorrect_count,
                    'total_attempts': total_count,
                    'accuracy': round(accuracy, 1)
                })
        
        return questions
    
    @staticmethod
    def get_user_statistics(user_id):
        """ユーザーの学習統計情報を取得"""
        try:
            # すべての解答を取得
            all_answers = UserAnswer.query.filter_by(user_id=user_id).all()
            
            if not all_answers:
                return {
                    'total_answers': 0,
                    'total_correct': 0,
                    'total_incorrect': 0,
                    'average_accuracy': 0,
                    'today_answers': 0,
                    'today_correct': 0,
                    'today_accuracy': 0,
                    'week_answers': 0,
                    'week_correct': 0,
                    'week_accuracy': 0,
                    'consecutive_days': 0,
                    'unique_questions': 0,
                    'total_questions': Question.query.count(),
                    'progress_percentage': 0,
                    'category_stats': {},
                    'last_study_date': None
                }
            
            # 基本統計
            total_answers = len(all_answers)
            total_correct = sum(1 for a in all_answers if a.is_correct)
            total_incorrect = total_answers - total_correct
            average_accuracy = (total_correct / total_answers * 100) if total_answers > 0 else 0
            
            # 今日の統計
            today = datetime.utcnow().date()
            today_start = datetime.combine(today, datetime.min.time())
            today_answers = [a for a in all_answers if a.timestamp >= today_start]
            today_answers_count = len(today_answers)
            today_correct = sum(1 for a in today_answers if a.is_correct)
            today_accuracy = (today_correct / today_answers_count * 100) if today_answers_count > 0 else 0
            
            # 今週の統計
            week_start = today_start - timedelta(days=7)
            week_answers = [a for a in all_answers if a.timestamp >= week_start]
            week_answers_count = len(week_answers)
            week_correct = sum(1 for a in week_answers if a.is_correct)
            week_accuracy = (week_correct / week_answers_count * 100) if week_answers_count > 0 else 0
            
            # 連続学習日数の計算
            study_dates = set()
            for answer in all_answers:
                study_date = answer.timestamp.date()
                study_dates.add(study_date)
            
            consecutive_days = 0
            if study_dates:
                sorted_dates = sorted(study_dates, reverse=True)
                current_date = datetime.utcnow().date()
                
                # 今日学習していない場合は、昨日からカウント
                if current_date not in sorted_dates:
                    current_date = current_date - timedelta(days=1)
                
                check_date = current_date
                for study_date in sorted_dates:
                    if study_date == check_date:
                        consecutive_days += 1
                        check_date = check_date - timedelta(days=1)
                    else:
                        break
            
            # 学習した問題数（ユニーク）
            unique_questions = len(set(a.question_id for a in all_answers))
            total_questions = Question.query.count()
            progress_percentage = (unique_questions / total_questions * 100) if total_questions > 0 else 0
            
            # カテゴリ別統計
            category_stats = {}
            for answer in all_answers:
                question = Question.query.get(answer.question_id)
                if question:
                    category = question.category
                    if category not in category_stats:
                        category_stats[category] = {
                            'total': 0,
                            'correct': 0,
                            'accuracy': 0
                        }
                    category_stats[category]['total'] += 1
                    if answer.is_correct:
                        category_stats[category]['correct'] += 1
            
            # カテゴリ別の正答率を計算
            for category in category_stats:
                stats = category_stats[category]
                stats['accuracy'] = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
                stats['accuracy'] = round(stats['accuracy'], 1)
            
            # 最後の学習日
            last_study_date = max(a.timestamp.date() for a in all_answers) if all_answers else None
            
            return {
                'total_answers': total_answers,
                'total_correct': total_correct,
                'total_incorrect': total_incorrect,
                'average_accuracy': round(average_accuracy, 1),
                'today_answers': today_answers_count,
                'today_correct': today_correct,
                'today_accuracy': round(today_accuracy, 1),
                'week_answers': week_answers_count,
                'week_correct': week_correct,
                'week_accuracy': round(week_accuracy, 1),
                'consecutive_days': consecutive_days,
                'unique_questions': unique_questions,
                'total_questions': total_questions,
                'progress_percentage': round(progress_percentage, 1),
                'category_stats': category_stats,
                'last_study_date': last_study_date.isoformat() if last_study_date else None
            }
        except Exception as e:
            print(f"Error in get_user_statistics: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
