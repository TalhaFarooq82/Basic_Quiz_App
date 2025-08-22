def get_feedback(score, total):
    percentage = (score / total) * 100
    if percentage >= 90:
        return "Excellent work! You're mastering this topic."
    elif percentage >= 70:
        return "Good job! Keep practicing to improve more."
    elif percentage >= 50:
        return "Not bad, but review the concepts again."
    else:
        return "You might need to revisit the topic. Don’t give up!"