# Basic_Quiz_App 🎯

## 📌 Overview
The **Basic Quiz App** is a Flask-based web application that allows admins to create quizzes and users to attempt them. It also includes authentication, AI-generated hints/feedback, and performance tracking.  

## 🚀 Features
- 🔑 User Authentication (Login/Signup)  
- 🛠️ Admin Panel for managing quizzes and questions  
- 📝 Quiz Creation & Attempt  
- 📊 Performance Tracking with results  
- 🤖 AI Assistance (Hints & Feedback)  
- 🎨 Simple CSS Styling  

## 📂 Project Structure
```text
Basic_Quiz_App/
│── run.py                # Entry point
│── config.py             # App configuration
│── app/
│   ├── __init__.py       # Flask app factory
│   ├── models.py         # Database models
│   ├── questions.csv     # Sample quiz questions
│   ├── ai/               # AI logic (feedback & hints)
│   ├── routes/           # Routes (Admin, Auth, Quiz)
│   ├── Static/           # CSS & static files
