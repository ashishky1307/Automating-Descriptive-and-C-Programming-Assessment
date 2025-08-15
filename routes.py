from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from models import Student, db, Questions, StudentAnswer, Evaluation, QuestionPaper, QuestionPaperQuestion, Evaluator
from utils import calculate_summary, save_evaluation_results, calculate_similarity, count_grammar_mistakes, word_count, load_model, load_dataset, load_tokenizer, evaluate_student_answers
from utils import evaluate_errors, run_c_program, classify_errors, calculate_marks
import logging
import os
import subprocess

main = Blueprint('main', __name__)

# Authentication Routes
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        login_id = request.form.get('login_id')
        password = request.form.get('password')
        remember_me = 'remember_me' in request.form
        
        user = None
        
        if user_type == 'student':
            user = Student.query.filter_by(student_id=login_id).first()
        elif user_type == 'evaluator':
            user = Evaluator.query.filter_by(employee_id=login_id).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            next_page = request.args.get('next')
            
            if user_type == 'student':
                return redirect(next_page) if next_page else redirect(url_for('main.student_dashboard', student_id=user.id))
            else:
                return redirect(next_page) if next_page else redirect(url_for('main.evaluator_dashboard'))
        else:
            flash('Invalid login credentials. Please try again.', 'error')
    
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if user_type == 'student':
            existing_user = Student.query.filter((Student.student_id == user_id) | (Student.email == email)).first()
            if existing_user:
                flash('Student ID or email already exists.', 'error')
                return render_template('register.html')
            
            # Create new student
            new_user = Student(
                student_id=user_id,
                name=name,
                email=email,
                phone=phone,
                course=request.form.get('course'),
                semester=request.form.get('semester')
            )
        else:
            existing_user = Evaluator.query.filter((Evaluator.employee_id == user_id) | (Evaluator.email == email)).first()
            if existing_user:
                flash('Employee ID or email already exists.', 'error')
                return render_template('register.html')
            
            # Create new evaluator
            new_user = Evaluator(
                employee_id=user_id,
                name=name,
                email=email,
                phone=phone,
                department=request.form.get('department'),
                designation=request.form.get('designation')
            )
        
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.home'))

@main.route('/forgot_password')
def forgot_password():
    # TODO: Implement password reset functionality
    flash('Password reset functionality will be available soon.', 'info')
    return redirect(url_for('main.login'))


@main.route('/')
def home():
    return render_template("home.html")

@main.route('/submit_marks', methods=['POST'])
@login_required
def submit_marks():
    student_id = request.form.get('student_id')
    question_id = request.form.get('question_id')
    marks = request.form.get('marks')
    
    evaluation = Evaluation.query.filter_by(student_id=student_id, question_id=question_id).first()
    if evaluation:
        evaluation.predicted_marks = marks
    else:
        new_evaluation = Evaluation(
            student_id=student_id,
            question_id=question_id,
            similarity=0,
            grammar_mistakes=0,
            word_count=0,
            keywords=0,
            marks=marks
        )
        db.session.add(new_evaluation)
    
    db.session.commit()
    return redirect(url_for('main.view_answers', student_id=student_id))

@main.route('/evaluator_dashboard')
@login_required
def evaluator_dashboard():
    if not isinstance(current_user, Evaluator):
        flash('Access denied. Evaluator privileges required.', 'error')
        return redirect(url_for('main.home'))
    students = Student.query.all()
    return render_template('evaluator_dashboard.html', students=students)

@main.route('/view_evaluation/<int:student_id>/<int:question_id>')
@login_required
def view_evaluation(student_id, question_id):
    student = Student.query.get_or_404(student_id)
    question = Questions.query.get_or_404(question_id)
    answers = StudentAnswer.query.filter_by(student_id=student_id, question_id=question_id).all()
    return render_template('view_evaluation.html', student=student, question=question, answers=answers)

@main.route('/view_answers/<int:student_id>')
@login_required
def view_answers(student_id):
    student = Student.query.get_or_404(student_id)
    answers = StudentAnswer.query.filter_by(student_id=student_id).all()
    evaluations = Evaluation.query.filter_by(student_id=student_id).all()
    
    # Debugging
    print(f'Student: {student.name}, ID: {student_id}, Answers: {len(answers)}, Evaluations: {len(evaluations)}')

    evaluations_dict = {e.question_id: e for e in evaluations}
    
    total_marks = sum(evaluations_dict.get(answer.question_id, Evaluation()).predicted_marks or 0 for answer in answers)
    
    return render_template(
        'view_answers.html',
        student=student,
        answers=answers,
        evaluations_dict=evaluations_dict,
        total_marks=total_marks,
        student_id=student_id  # Ensure this line is included

    )


@main.route('/calculate_totals', methods=['POST'])
def calculate_totals():
    students = Student.query.all()
    
    for student in students:
        evaluations = Evaluation.query.filter_by(student_id=student.id).all()
        if not evaluations:
            continue  # Skip if no evaluations found

        total_score = sum(evaluation.predicted_marks or 0 for evaluation in evaluations)
        
        # Debugging print
        print(f"Student ID: {student.id}, Total Score: {total_score}")

        # Update student's final score
        student.final_score = total_score
        db.session.commit()

    return redirect(url_for('main.evaluator_dashboard'))

# Route to render the form for adding a question
@main.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question_text = request.form['question_text']
        model_answer = request.form['model_answer']
        evaluator_id = 1  # Assuming logged-in evaluator with ID 1 for demo purposes

        # Create a new Question instance and save to the database
        new_question = Questions(question_text=question_text, model_answer=model_answer, created_by=evaluator_id)
        db.session.add(new_question)
        db.session.commit()
        flash('Question added successfully!', 'success')
        return redirect(url_for('main.add_question'))
    
    return render_template('add_question.html')
@main.route('/student_view_exam/<int:paper_id>/<int:student_id>', methods=['GET', 'POST'])
def student_view_exam(paper_id, student_id):
    # Get the student and question paper objects from the database
    student = Student.query.get_or_404(student_id)
    question_paper = QuestionPaper.query.get_or_404(paper_id)

    # Fetch the questions for the exam
    questions = Questions.query.join(
        QuestionPaperQuestion,
        Questions.id == QuestionPaperQuestion.question_id
    ).filter(
        QuestionPaperQuestion.question_paper_id == paper_id
    ).all()

    if request.method == 'POST':
        # Fetch the answers and question IDs from the form
        answers = {}
        for key, value in request.form.items():
            if key.startswith('answers_'):
                question_id = int(key.split('_')[1])  # Extract the question ID from the field name
                answers[question_id] = value

        # Now save the answers to the StudentAnswer table
        for question_id, answer_text in answers.items():
            new_answer = StudentAnswer(
                student_id=student_id,
                question_id=question_id,
                answer_text=answer_text
            )
            db.session.add(new_answer)
        
        db.session.commit()  # Commit all new answers to the database

        flash("Answers submitted successfully!", "success")
          # Redirect to some page after submission

    # Render the template with the necessary data if not POST (GET request)
    return render_template('student_view_exam.html', 
                           question_paper=question_paper, 
                           questions=questions, 
                           student=student, 
                           student_id=student_id)





@main.route('/student_dashboard/<int:student_id>')
def student_dashboard(student_id):
    # Get student information
    student = Student.query.filter_by(id=student_id).first()    
    print("Student Info:", student)  # Print student info
   # Get available exams for the student
    available_exams = QuestionPaper.query.all()
    print("Available Exams:", available_exams)  # Print available exams

    # Get student's exam results
    student_results =Student.query.filter_by(id=student_id).first()    
    print("Student Results:", student_results)  # Print student results

    return render_template('student_dashboard.html', 
                           student=student, 
                           available_exams=available_exams,
                           student_results=student_results)

@main.route('/start_exam', methods=['POST'])
def start_exam():
    student_id = request.form['student_id']
    exam_id = request.form['exam_id']
    
    # Logic to start the exam for the student
    return redirect(url_for('main.take_exam', exam_id=exam_id, student_id=student_id))







@main.route('/student_exam_dashboard', methods=['GET', 'POST'])
def student_exam_dashboard():
    student_id = 0
    error_message = None
    question_papers = []

    if request.method == 'POST':
        student_id = request.form['student_id'].strip()

        # Check if the student exists in the database
        student = Student.query.filter_by(id=student_id).first()
        print(student)
        if student:
            # If the student exists, fetch the available question papers
            question_papers = QuestionPaper.query.all()
        else:
            # If student doesn't exist, set an error message
            error_message = f"Student '{student_id}' not found in the system."

    return render_template('student_exam_dashboard.html', 
                           question_papers=question_papers, 
                           student_id=student_id,
                           error_message=error_message)

@main.route('/create_question_paper', methods=['GET', 'POST'])
def create_question_paper():
    if request.method == 'POST':
        paper_name = request.form['paper_name']
        selected_questions = request.form.getlist('questions')
        evaluator_id = 1  # Assuming logged-in evaluator with ID 1 for demo purposes

        # Create a new QuestionPaper instance and save to the database
        new_paper = QuestionPaper(paper_name=paper_name, evaluator_id=evaluator_id)
        db.session.add(new_paper)
        db.session.commit()  # Commit to get the new paper's ID

        # Debugging: Print selected questions to verify
        print(f"Selected questions: {selected_questions}")

        # Add selected questions to the question paper
        for question_id in selected_questions:
            question_id = int(question_id)  # Ensure it's an integer
            
            # Ensure question exists before adding it to the question paper
            question = Questions.query.get(question_id)
            if not question:
                flash(f"Question with id {question_id} does not exist", 'error')
                continue  # Skip to the next question if not found

            # Check if the question is already associated with the paper
            existing_association = QuestionPaperQuestion.query.filter_by(question_paper_id=new_paper.id, question_id=question_id).first()
            if not existing_association:
                paper_question = QuestionPaperQuestion(question_paper_id=new_paper.id, question_id=question_id)
                db.session.add(paper_question)
            else:
                flash(f"Question with id {question_id} is already added to this paper.", 'info')

        db.session.commit()  # Commit all additions at once
        flash("Question paper created successfully.", 'success')
        return redirect(url_for('main.create_question_paper'))

    # Fetch all available questions for the evaluator to choose from
    questions = Questions.query.all()
    flash("Question paper created successfully.", 'success')
        
    return render_template('create_paper.html', questions=questions)
    
def get_student_results(student_id):
    # Query to join StudentAnswer, Question, and Evaluation tables to fetch the required data
    results = db.session.query(StudentAnswer, Questions.question_text, Evaluation.predicted_marks)\
        .join(Questions, StudentAnswer.question_id == Questions.id)\
        .join(Evaluation, StudentAnswer.id == Evaluation.student_id)\
        .filter(StudentAnswer.student_id == student_id).all()
    
    # Fetch final score of the student from the Student table
    final_score = db.session.query(Student.final_score)\
        .filter(Student.id == student_id).first()
    
    return results, final_score

@main.route('/view_results/<int:student_id>')
def view_results(student_id):
    # Get student results and final score from the database
    student_results, final_score = get_student_results(student_id)

    # Debugging: Print the fetched results
    print(student_results)  # Check if this contains the expected results
    print(final_score)      # Check if final_score is being fetched correctly

    # Calculate total marks from the predicted marks
    total_marks = sum([result.predicted_marks for result in student_results])

    # Pass the results, total marks, and final score to the HTML template
    return render_template('student_results.html', 
                            student_id=student_id,   # Ensure student_id is passed to the template
                            results=student_results, 
                            total_marks=total_marks, 
                            final_score=final_score[0])

# Load model and tokenizer once at the start
model = load_model()
tokenizer = load_tokenizer()
ds = load_dataset()  # Only if ds doesn't change between requests
from flask import flash
max_seq_length=100
from tf_keras.preprocessing.sequence import pad_sequences
@main.route('/view_metrics/<int:student_id>/<int:question_id>', methods=['GET', 'POST'])

def view_metrics(student_id, question_id):
    answer_record = StudentAnswer.query.filter_by(student_id=student_id, question_id=question_id).first()
    question_record = Questions.query.filter_by(id=question_id).first()

    if not answer_record or not question_record:
        return "Answer or question not found", 404

    student_answer = answer_record.answer_text
    model_answer = question_record.model_answer

    try:
        # Fetch the existing evaluation record or create a new one if it doesn't exist
        evaluation_record = Evaluation.query.filter_by(student_id=student_id, question_id=question_id).first()

        # Log if the record is found or not
        logging.debug(f"Evaluation Record: {evaluation_record}")

        # Compute evaluation metrics
        summary_result = calculate_summary(student_answer)
        similarity_result = calculate_similarity(model_answer, student_answer)
        grammar_mistakes = count_grammar_mistakes(student_answer)
        word_count_result = word_count(student_answer)

        # Ensure similarity_result and word_count_result are valid numbers
        if not isinstance(similarity_result, (int, float)):
            raise ValueError("Similarity result is not a valid number")
        
        if not isinstance(word_count_result, int):
            raise ValueError("Word count result is not a valid integer")

        # Apply the thresholds for predicted marks
        predicted_marks = max(0, min(10, (similarity_result * 0.5 + word_count_result * 0.3 + (100 - grammar_mistakes) * 0.2)))

        if similarity_result <= 35:
            predicted_marks = 0
        if word_count_result <= 6:
            predicted_marks = 0

        # If no evaluation record, create one
        if not evaluation_record:
            evaluation_record = Evaluation(
                student_id=student_id,
                question_id=question_id,
                similarity=similarity_result,
                grammar_mistakes=grammar_mistakes,
                word_count=word_count_result,
                summary=summary_result,
                predicted_marks=predicted_marks
            )
            db.session.add(evaluation_record)
            flash('Evaluation created successfully!', 'success')
        else:
            # Update existing evaluation record
            evaluation_record.similarity = similarity_result
            evaluation_record.grammar_mistakes = grammar_mistakes
            evaluation_record.word_count = word_count_result
            evaluation_record.summary = summary_result
            evaluation_record.predicted_marks = predicted_marks
            flash('Evaluation updated successfully!', 'success')

        db.session.commit()

    except Exception as e:
        logging.error(f"Error during evaluations: {e}")
        return "An error occurred during evaluation.", 500

    # Handle POST request to update marks
    if request.method == 'POST':
        new_marks = request.form.get('marks', type=int)

        # Update marks in the database
        evaluation_record.predicted_marks = new_marks
        db.session.commit()
        flash('Marks updated successfully!', 'success')

    # Log after committing the session to verify update
    logging.debug(f"Updated Evaluation Record: {evaluation_record.predicted_marks}")

    # Prepare evaluation data for display
    evaluation = {
        "similarity": evaluation_record.similarity,
        "grammar_mistakes": evaluation_record.grammar_mistakes,
        "word_count": evaluation_record.word_count,
        "summary": evaluation_record.summary,
        "predicted_marks": evaluation_record.predicted_marks
    }

    # Return the evaluation data to the frontend
    return render_template('after.html', answer=answer_record, evaluation=evaluation)

@main.route('/view_exam_results/<int:student_id>/<int:paper_id>')
def view_exam_results(student_id, paper_id):
    # Fetch the student and question paper details
    student = Student.query.get_or_404(student_id)
    question_paper = QuestionPaper.query.get_or_404(paper_id)
    
    # Fetch the questions included in the question paper
    questions = db.session.query(Questions).join(
        QuestionPaperQuestion,
        Questions.id == QuestionPaperQuestion.question_id
    ).filter(
        QuestionPaperQuestion.question_paper_id == paper_id
    ).all()

    # Fetch all answers provided by the student for the question paper
    student_answers = StudentAnswer.query.filter_by(student_id=student_id).all()
    
    # Fetch evaluations for the student's answers
    evaluations = Evaluation.query.filter_by(student_id=student_id).all()

    # Create a dictionary to store evaluations for easier lookup
    evaluations_dict = {e.question_id: e for e in evaluations}
    
    # Prepare result data to be displayed
    results = []
    total_marks = 0
    
    for question in questions:
        answer_record = next((ans for ans in student_answers if ans.question_id == question.id), None)
        evaluation_record = evaluations_dict.get(question.id)
        
        # Default values if no record found
        student_answer = answer_record.answer_text if answer_record else "No answer provided"
        predicted_marks = evaluation_record.predicted_marks if evaluation_record else 0
        total_marks += predicted_marks  # Sum up total marks

        # Add the result data
        results.append({
            "question_text": question.question_text,
            "model_answer": question.model_answer,
            "student_answer": student_answer,
            "predicted_marks": predicted_marks,
            "similarity": evaluation_record.similarity if evaluation_record else 0,
            "grammar_mistakes": evaluation_record.grammar_mistakes if evaluation_record else 0,
            "word_count": evaluation_record.word_count if evaluation_record else 0
        })

    # Render the results template with the fetched data
    return render_template(
        'exam_results.html',
        student=student,
        question_paper=question_paper,
        results=results,
        total_marks=total_marks
    )

@main.route('/up')
def up():
    return render_template('upload.html')
SAVE_DIR = 'C:/workspaces/error_log/test'

# Ensure the directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

@main.route('/upload', methods=['POST'])
def upload():
    c_code = request.form.get('c_code')
    input_file = request.files.get('input_file')

    # Validate C code for security
    if c_code:
        from utils import validate_c_code, sanitize_input
        
        # Sanitize the input
        c_code = sanitize_input(c_code)
        
        # Validate for security
        is_valid, validation_message = validate_c_code(c_code)
        if not is_valid:
            flash(f'Code validation failed: {validation_message}', 'error')
            return render_template('upload.html')

    # Paths for saving the files
    code_file_path = 'C:/workspaces/error_log/test/code.c'
    input_file_path = 'C:/workspaces/error_log/test/input.txt'

    # Save the C code to a file
    if c_code:
        with open(code_file_path, 'w', encoding='utf-8') as code_file:
            code_file.write(c_code)

    # Save the uploaded input file
    if input_file:
        input_file.save(input_file_path)

    # Compile and run the C program
    status, message = run_c_program(code_file_path)

    if status in ['Compilation Error', 'Runtime Error']:
        marks = calculate_marks(message)
        return render_template('result.html', status=status, message=message, marks=marks)
    else:
        return render_template('result.html', status=status, message=message, marks=10)
