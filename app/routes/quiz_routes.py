from flask import Blueprint,flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Question, Result
from app import db
from datetime import datetime
from app.ai.feedback import get_feedback
from app.ai.hints import get_hint
from sqlalchemy import distinct
import matplotlib.pyplot as plt
import os
import uuid

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/')
@login_required
def dashboard():
    topics = [row[0] for row in db.session.query(distinct(Question.topic)).all()]
    difficulties = ["Easy", "Medium", "Hard"]

    # ✅ Only admins need the full list of questions
    questions = Question.query.all() if current_user.role == 'admin' else []

    return render_template(
        'dashboard.html',
        topics=topics,
        difficulties=difficulties,
        questions=questions
    )



@quiz_bp.route('/start-quiz', methods=['POST'])
@login_required
def start_quiz():
    if current_user.role != 'student':
        flash("Admins cannot attempt quizzes.", "danger")
        return redirect(url_for('quiz.dashboard'))

    topic = request.form.get('topic')
    difficulty = request.form.get('difficulty')
    questions = Question.query.filter_by(topic=topic, difficulty=difficulty).all()
    return render_template('quiz.html', questions=questions, get_hint=get_hint, topic=topic, difficulty=difficulty)


@quiz_bp.route('/submit-quiz', methods=['POST'])
@login_required
def submit_quiz():
    questions = Question.query.filter(Question.id.in_(request.form.keys())).all()
    score = 0
    for q in questions:
        if request.form.get(str(q.id)) == q.correct_option:
            score += 1

    result = Result(    
        user_id=current_user.id,
        score=score,
        total=len(questions),
        topic=request.form.get('topic'),
        date=datetime.now()
    )
    db.session.add(result)
    db.session.commit()

    # ✅ Create pie chart
    correct = score
    incorrect = len(questions) - score
    labels = ['Correct', 'Incorrect']
    values = [correct, incorrect]
    colors = ['#4CAF50', '#F44336']

    plt.figure(figsize=(4, 4))
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title('Quiz Performance')

    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join("app", "static", "charts", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    plt.savefig(filepath)
    plt.close()

    feedback = get_feedback(score, len(questions))

    summary = []
    for q in questions:
        user_ans = request.form.get(str(q.id))
        summary.append({
            'question': q.text,
            'your_answer': user_ans,
            'correct_answer': q.correct_option,
            'is_correct': user_ans == q.correct_option
        })

    return render_template(
        'result.html',
        score=score,
        total=len(questions),
        feedback = feedback,
        chart_filename = filename,
        summary = summary
    )