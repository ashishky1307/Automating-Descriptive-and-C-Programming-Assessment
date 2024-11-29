from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_text = db.Column(db.Text, nullable=False)
    model_answer = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    answers = db.relationship('StudentAnswer', back_populates='question')
    evaluations = db.relationship('Evaluation', back_populates='question')


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    final_score = db.Column(db.Float)

    answers = db.relationship('StudentAnswer', back_populates='student')  # Add this line


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
