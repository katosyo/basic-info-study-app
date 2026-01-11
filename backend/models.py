from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    answers = db.relationship('UserAnswer', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Option(db.Model): # OptionをQuestionより前に移動
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    option_text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Option {self.id}: {self.option_text[:30]}...>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False) # 例: 'multiple_choice', 'true_false'
    category = db.Column(db.String(100), nullable=False) # 例: 'ネットワーク', 'データベース'
    difficulty = db.Column(db.String(50), nullable=False) # 例: 'easy', 'medium', 'hard'
    explanation = db.Column(db.Text, nullable=True) # 解説
    correct_option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=True) # 小文字の'option.id'に戻す
    options = db.relationship('Option', backref='question', lazy=True, cascade='all, delete-orphan', primaryjoin='Question.id == Option.question_id') # primaryjoinを明示的に指定
    answers = db.relationship('UserAnswer', backref='question', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Question {self.id}: {self.question_text[:30]}...>'

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=True) # 選択しなかった場合はNone
    is_correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserAnswer {self.id}: User {self.user_id} - Question {self.question_id} ({self.is_correct})>'
