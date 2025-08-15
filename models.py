from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class UserMixin:
    """Simple UserMixin implementation for Flask-Login compatibility"""
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return getattr(self, 'is_active', True)
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_text = db.Column(db.Text, nullable=False)
    model_answer = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    answers = db.relationship('StudentAnswer', back_populates='question')
    evaluations = db.relationship('Evaluation', back_populates='question')


class Student(db.Model, UserMixin):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)  # Student registration number
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    course = db.Column(db.String(100))
    semester = db.Column(db.String(20))
    final_score = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    answers = db.relationship('StudentAnswer', back_populates='student')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<Student {self.name}>'


class Evaluator(db.Model, UserMixin):
    __tablename__ = 'evaluators'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)  # Employee ID
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<Evaluator {self.name}>'


class StudentAnswer(db.Model):
    __tablename__ = 'student_answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    marks = db.Column(db.Float)
    student = db.relationship('Student', back_populates='answers')
    question = db.relationship('Questions', back_populates='answers')


class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    similarity = db.Column(db.Float, nullable=True)
    grammar_mistakes = db.Column(db.Float, nullable=True)
    word_count = db.Column(db.Float, nullable=True)
    predicted_marks = db.Column(db.Float, nullable=True)
    summary = db.Column(db.Text)

    question = db.relationship('Questions', back_populates='evaluations')


class QuestionPaper(db.Model):
    __tablename__ = 'question_paper'
    id = db.Column(db.Integer, primary_key=True)
    paper_name = db.Column(db.String(255), nullable=False)
    evaluator_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship('QuestionPaperQuestion', backref='question_paper')


class QuestionPaperQuestion(db.Model):
    __tablename__ = 'question_paper_question'
    id = db.Column(db.Integer, primary_key=True)
    question_paper_id = db.Column(db.Integer, db.ForeignKey('question_paper.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
