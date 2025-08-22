from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Question
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('quiz.dashboard'))

    # ✅ Get all questions from DB and pass to template
    questions = Question.query.all()
    return render_template('dashboard.html', questions=questions)


@admin_bp.route('/add-question', methods=['GET', 'POST'])
@login_required
def add_question():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('quiz.dashboard'))

    if request.method == 'POST':
        # Get form data
        question_text = request.form['question_text']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_option = request.form['correct_option']
        topic = request.form['topic']
        difficulty = request.form['difficulty']

        # Create new Question object
        new_question = Question(
            text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option,
            topic=topic,
            difficulty=difficulty
        )

        # Add to database
        db.session.add(new_question)
        db.session.commit()
        flash('Question added successfully!')
        return redirect(url_for('admin.add_question'))

    return render_template('admin/add_question.html')


#-------------------------------------TO add question through CSV--------------------------------
import csv
from io import TextIOWrapper

@admin_bp.route('/upload-csv', methods=['POST'])
@login_required
def upload_csv():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('quiz.dashboard'))

    file = request.files['csv_file']
    if not file.filename.endswith('.csv'):
        flash('Please upload a CSV file.', 'danger')
        return redirect(url_for('quiz.dashboard'))

    try:
        # Read and parse CSV file
        stream = TextIOWrapper(file.stream, encoding='utf-8')
        reader = csv.DictReader(stream)

        for row in reader:
            # Skip if question already exists
            existing = Question.query.filter_by(text=row['question_text']).first()
            if existing:
                continue


            new_question = Question(
                text=row['question_text'],
                option_a=row['option_a'],
                option_b=row['option_b'],
                option_c=row['option_c'],
                option_d=row['option_d'],
                correct_option=row['correct_option'],
                topic=row['topic'],
                difficulty=row['difficulty']
            )
            db.session.add(new_question)

        db.session.commit()
        flash('Questions uploaded from CSV successfully!', 'success')

    except Exception as e:
        flash(f'Error uploading CSV: {str(e)}', 'danger')

    return redirect(url_for('quiz.dashboard'))



# ----------------------------------DELETE Quesiton-------------------------------

@admin_bp.route('/delete-question/<int:question_id>', methods=['POST'])
@login_required
def delete_question(question_id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('quiz.dashboard'))

    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully.', 'success')
    return redirect(url_for('admin.admin_dashboard'))
