"""
Database setup script for the Assessment System
This script creates all necessary tables in your cloud database
"""

from flask import Flask
from models import db, Student, Questions, Evaluator, Evaluation, StudentAnswer, QuestionPaper, QuestionPaperQuestion
from config import Config
import sys

def create_database_tables():
    """Create all database tables"""
    print("🔧 Setting up database tables...")
    
    try:
        # Create Flask app instance
        app = Flask(__name__)
        app.config.from_object(Config)
        
        # Initialize database
        db.init_app(app)
        
        with app.app_context():
            print(f"📡 Connecting to database: {Config.SQLALCHEMY_DATABASE_URI[:50]}...")
            
            # Drop and recreate all tables for fresh start
            print("🗑️ Dropping existing tables...")
            db.drop_all()
            
            # Create all tables
            print("🏗️ Creating new tables...")
            db.create_all()
            print("✅ All tables created successfully!")
            
            # Create default users
            print("👥 Creating default users...")
            
            # Create admin evaluator
            admin_evaluator = Evaluator(
                employee_id='ADMIN001',
                name='Admin Evaluator',
                email='admin@assessment.com',
                phone='+1234567890',
                department='Computer Science',
                designation='System Administrator',
                is_admin=True
            )
            admin_evaluator.set_password('admin123')
            
            # Create sample student
            sample_student = Student(
                student_id='STU001',
                name='John Doe',
                email='john.doe@student.com',
                phone='+1234567891',
                course='Computer Science',
                semester='6'
            )
            sample_student.set_password('student123')
            
            # Create sample evaluator
            sample_evaluator = Evaluator(
                employee_id='EMP001',
                name='Jane Smith',
                email='jane.smith@faculty.com',
                phone='+1234567892',
                department='Computer Science',
                designation='Assistant Professor'
            )
            sample_evaluator.set_password('evaluator123')
            
            # Add sample users
            db.session.add(admin_evaluator)
            db.session.add(sample_student)
            db.session.add(sample_evaluator)
            
            # Create sample question
            sample_question = Questions(
                question_text="Explain the concept of Object-Oriented Programming and its key principles.",
                model_answer="Object-Oriented Programming (OOP) is a programming paradigm based on the concept of objects. The key principles include: 1) Encapsulation - bundling data and methods together, 2) Inheritance - creating new classes based on existing ones, 3) Polymorphism - using a single interface for different underlying forms, 4) Abstraction - hiding complex implementation details.",
                created_by=1  # Admin evaluator
            )
            
            db.session.add(sample_question)
            
            # Commit all changes
            db.session.commit()
            
            # Verify setup
            students_count = Student.query.count()
            questions_count = Questions.query.count()
            evaluators_count = Evaluator.query.count()
            
            print(f"📊 Database Status:")
            print(f"   - Students: {students_count}")
            print(f"   - Questions: {questions_count}")
            print(f"   - Evaluators: {evaluators_count}")
            
            print("\n� Default Login Credentials:")
            print("🔑 Admin Evaluator - ID: ADMIN001, Password: admin123")
            print("🎓 Sample Student - ID: STU001, Password: student123")
            print("👨‍🏫 Sample Evaluator - ID: EMP001, Password: evaluator123")
            
            print("🎉 Database setup completed successfully!")
            
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        print(f"🔍 Error details: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    create_database_tables()
