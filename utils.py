import subprocess
import logging
import re
import os
from collections import Counter
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import language_tool_python
import pandas as pd
import pickle
import nltk
import spacy
from tensorflow.keras.preprocessing.sequence import pad_sequences
from transformers import pipeline
from models import StudentAnswer, Questions, db ,Evaluation

# Security function for validating C code
def validate_c_code(code):
    """
    Validate C code for security issues before compilation
    """
    dangerous_functions = [
        'system', 'exec', 'popen', 'fork', 'exit',
        'remove', 'unlink', 'rmdir', 'chmod'
    ]
    
    dangerous_includes = [
        'windows.h', 'sys/socket.h', 'netinet/in.h'
    ]
    
    # Check for dangerous functions
    for func in dangerous_functions:
        if func in code:
            return False, f"Dangerous function '{func}' detected"
    
    # Check for dangerous includes
    for include in dangerous_includes:
        if include in code:
            return False, f"Potentially dangerous include '{include}' detected"
    
    # Check for excessive file operations
    if code.count('fopen') > 3:
        return False, "Too many file operations detected"
    
    return True, "Code validation passed"

# Input sanitization function
def sanitize_input(text, max_length=10000):
    """
    Sanitize user input to prevent injection attacks
    """
    if not text:
        return ""
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove potentially dangerous patterns
    dangerous_patterns = [
        r'<script.*?</script>',
        r'javascript:',
        r'vbscript:',
        r'onload=',
        r'onerror=',
        r'eval\(',
        r'exec\('
    ]
    
    for pattern in dangerous_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    return text.strip()
       
sentence_model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
tool = language_tool_python.LanguageTool('en-US')
from models import Evaluation  # Import the Evaluation model
# Ensure that all required arguments are passed to the functions

def save_evaluation_results(student_id, question_id, summary, similarity, grammar_mistakes, word_count, predicted_marks):
    try:
        # Check if an evaluation record already exists
        evaluation_record = Evaluation.query.filter_by(student_id=student_id, question_id=question_id).first()

        if evaluation_record:
            # Update existing record
            evaluation_record.similarity = similarity
            evaluation_record.grammar_mistakes = grammar_mistakes
            evaluation_record.word_count = word_count
            evaluation_record.predicted_marks = predicted_marks
            evaluation_record.summary = summary
            db.session.commit()
            logging.info(f"Updated evaluation for student {student_id}, question {question_id}")
        else:
            # Create a new record if none exists
            evaluation_record = Evaluation(
                student_id=student_id,
                question_id=question_id,
                similarity=similarity,
                grammar_mistakes=grammar_mistakes,
                word_count=word_count,
                predicted_marks=predicted_marks,
                summary=summary
            )
            db.session.add(evaluation_record)
            db.session.commit()
            logging.info(f"Created new evaluation for student {student_id}, question {question_id}")
    except Exception as e:
        logging.error(f"Error saving evaluation results: {e}")
        db.session.rollback()
        raise

def load_dataset(dataset_path='student_evaluation_results (2).csv'):
    df = pd.read_csv(dataset_path, encoding='ISO-8859-1')
    logging.info("Dataset loaded successfully.")
    return df

def load_model(model_path='answer_evaluation_model.pkl'):
    model = pickle.load(open(model_path, 'rb'))
    logging.info("Model loaded successfully.")
    return model

def load_tokenizer(tokenizer_path='tokenizer.pkl'):
    tokenizer = pickle.load(open(tokenizer_path, 'rb'))
    logging.info("Tokenizer loaded successfully.")
    return tokenizer
def evaluate_student_answers(student_id, question_id, model, tokenizer, max_seq_length, summary_result, similarity_result, grammar_mistakes, word_count_result):
    student_answers_data = StudentAnswer.query.filter_by(student_id=student_id).all()
    if not student_answers_data:
        return "No answers found for the given student ID"

    logging.debug(f"Number of answers fetched: {len(student_answers_data)}")

    questions = []
    student_answers = []

    for i, answer_data in enumerate(student_answers_data):
        question = str(answer_data.question_id)
        answer = answer_data.answer_text

        logging.debug(f"Question {i+1}: {question}")
        logging.debug(f"Answer {i+1}: {answer}")

        questions.append(question)
        student_answers.append(answer)

    question_seqs = tokenizer.texts_to_sequences(questions)
    answer_seqs = tokenizer.texts_to_sequences(student_answers)

    question_seqs = pad_sequences(question_seqs, maxlen=max_seq_length)
    answer_seqs = pad_sequences(answer_seqs, maxlen=max_seq_length)

    logging.debug(f"Question Sequences Shape: {question_seqs.shape}")
    logging.debug(f"Answer Sequences Shape: {answer_seqs.shape}")

    predicted_marks = model.predict([question_seqs, answer_seqs])
    predicted_marks = float(predicted_marks[0][0])
    predicted_marks = round(predicted_marks, 2)
    
    logging.debug(f"Predicted Marks: {predicted_marks}")
    
    save_evaluation_results(
        student_id=student_id,
        question_id=question_id,
        summary=summary_result,
        similarity=similarity_result,
        grammar_mistakes=grammar_mistakes,
        word_count=word_count_result,
        predicted_marks=predicted_marks
    )

    return f"{predicted_marks}"

def check_syntax_errors(c_code):
    try:
        with open("temp.c", "w") as f:
            f.write(c_code)
        
        result = subprocess.run(
            ["gcc", "-fsyntax-only", "temp.c"], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return result.stderr.decode('utf-8') if result.returncode != 0 else "No syntax errors detected."
    except Exception as e:
        logging.error(f"Error checking syntax: {e}")
        return "Error checking syntax."

def calculate_total_marks(predictions, max_marks_per_question):
    try:
        total_marks = sum(predictions)  # Assuming the model outputs a single value per answer
        return total_marks
    except Exception as e:
        logging.error(f"Error calculating total marks: {e}")
        return 0
from transformers import pipeline
import logging

from transformers import pipeline
import logging


from transformers import T5Tokenizer, T5ForConditionalGeneration
import logging

def calculate_summary(text, max_length=150, min_length=50, length_penalty=2.0):
    try:
        # Load pre-trained T5 model and tokenizer
        model = T5ForConditionalGeneration.from_pretrained('t5-large')
        tokenizer = T5Tokenizer.from_pretrained('t5-large')
        
        # Preprocess the text (T5 requires a prefix for summarization)
        input_text = "summarize: " + text
        inputs = tokenizer(input_text, return_tensors='pt', max_length=512, truncation=True)

        # Generate summary
        summary_ids = model.generate(inputs['input_ids'], 
                                     max_length=max_length, 
                                     min_length=min_length, 
                                     length_penalty=length_penalty,
                                     num_beams=4, 
                                     no_repeat_ngram_size=2, 
                                     early_stopping=True)

        # Decode the summary
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        logging.error(f"Error generating summary with T5: {e}")
        return "Error generating summary."


def calculate_similarity(model_answer, student_answer):
    
    logging.debug(f"Model Answer: {model_answer}")
    logging.debug(f"Student Answer: {student_answer}")
    
    if model_answer is None or student_answer is None:
        logging.error("One or both input answers are None.")
        return 0.0
    
    try:
        enc_model = sentence_model.encode(model_answer)
        enc_student = sentence_model.encode(student_answer)
        cos_sim = cosine_similarity([enc_model], [enc_student])
        similarity_score = cos_sim[0][0] * 100  # Convert to percentage
        return round(similarity_score, 2)
    except Exception as e:
        logging.error(f"Error calculating similarity: {e}")
        return 0.0

def count_grammar_mistakes(text):
    try:
        matches = tool.check(text)
        return len(matches)
    except Exception as e:
        logging.error(f"Error counting grammar mistakes: {e}")
        return 0

def word_count(text):
    try:
        return len(text.split())
    except Exception as e:
        logging.error(f"Error calculating word count: {e}")
        return 0



import subprocess
import os

def evaluate_errors(error_log):
    """
    Evaluates the error log and classifies errors into severity and type.
    
    Parameters:
    - error_log (str): The error log output from the compilation or runtime process.
    
    Returns:
    - dict: A dictionary with error details.
    """
    errors = {
        "total_errors": 0,
        "critical_errors": 0,
        "warnings": 0,
        "error_messages": []
    }

    # Example criteria: Counting critical errors and warnings
    for line in error_log.splitlines():
        if "error:" in line.lower():
            errors["total_errors"] += 1
            errors["critical_errors"] += 1
            errors["error_messages"].append(line)
        elif "warning:" in line.lower():
            errors["total_errors"] += 1
            errors["warnings"] += 1
            errors["error_messages"].append(line)
    
    return errors
import os
import subprocess

def run_c_program(file_path):
    try:
        # Save output to a directory with confirmed write permissions
        output_file_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'a.exe')
        
        gcc_path = 'C:/Users/DELL/Downloads/gcc-14.1.0-no-debug/bin/gcc-14.1.0.exe'

        # Compile the C program
        compile_process = subprocess.Popen(
            [gcc_path, '-o', output_file_path, file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = compile_process.communicate()

        # Check for compilation errors
        if compile_process.returncode != 0:
            error_log = stderr.decode('utf-8')
            return "Compilation Error", classify_errors(error_log)

        # Execute the compiled program
        run_process = subprocess.Popen(
            [output_file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        run_stdout, run_stderr = run_process.communicate()

        # Check for runtime errors
        if run_process.returncode != 0:
            runtime_error_log = run_stderr.decode('utf-8')
            return "Runtime Error", classify_errors(runtime_error_log, is_runtime=True)

        # If no errors, return success message and program output
        output = run_stdout.decode('utf-8').strip()
        return "Success", output

    except Exception as e:
        return "Runtime Error", str(e)
    
def classify_errors(error_log, is_runtime=False):
    error_details = {
        'total_errors': 0,
        'critical_errors': 0,
        'syntax_errors': 0,
        'warnings': 0,
        'error_messages': []
    }

    lines = error_log.split('\n')
    for line in lines:
        if 'error' in line.lower():
            error_details['total_errors'] += 1
            if 'critical' in line.lower():
                error_details['critical_errors'] += 1
            elif 'syntax' in line.lower():
                error_details['syntax_errors'] += 1
            else:
                error_details['warnings'] += 1
            error_details['error_messages'].append(line)
    
    if is_runtime:
        error_details['warnings'] += len(error_details['error_messages'])

    return error_details

def calculate_marks(error_details):
    max_marks = 10
    total_errors = error_details['total_errors']
    critical_errors = error_details['critical_errors']
    warnings = error_details['warnings']

    # Scoring rules
    if critical_errors > 0:
        return 0  # Critical errors lead to zero marks

    # Warning penalties
    marks = max_marks - (warnings * (max_marks * 0.2))
    marks = max(0, marks)  # Ensure non-negative marks
    return round(marks, 2)


