from app import create_app, db
from app.models import User, Question, Result

# First, create the app
app = create_app()

# ✅ Register this AFTER the app object is created
def create_tables():
    with app.app_context():
        db.create_all()

# Call it directly once at startup
create_tables()

if __name__ == '__main__':
    app.run(debug=True)
