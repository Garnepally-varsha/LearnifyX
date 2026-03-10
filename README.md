AI-Based Personalized Learning Path Generator

Overview

This project is a web application that generates a **personalized learning path for students** based on their interests, preferred learning style, and experience level.
The system collects user inputs through a questionnaire and uses an AI engine to recommend relevant learning materials.

The goal of this project is to help learners follow a **structured roadmap** instead of searching randomly for resources.

Features

* User **Signup and Login Authentication**
* Secure **password hashing**
* **Interactive questionnaire** to understand user goals
* AI-based **learning path generation**
* **Personalized course recommendations**
* **MongoDB database integration**
* Clean and responsive **frontend using HTML & CSS**

Tech Stack

Frontend

* HTML
* CSS

Backend

* Python
* Flask

Database

* MongoDB

Other Tools

* Git & GitHub
* Werkzeug (password hashing)
* Python Regex (validation)


How It Works

1. User signs up and logs into the system.
2. The system asks a series of questions:

   * Preferred learning domain (AI, DSA, Web Development, etc.)
   * Learning preference (videos, articles, projects)
   * Motivation or goal
   * Experience level (Beginner, Intermediate, Advanced)
3. The responses are stored in **MongoDB**.
4. The **AI engine processes the inputs** and generates a customized learning roadmap.
5. The recommended courses and resources are displayed on the learning path page.



Project Structure

```
project-folder
│
├── app.py                # Main Flask application
├── ai_engine.py          # AI logic for generating learning paths
├── mongodb.py            # MongoDB connection
│
├── templates/            # HTML files
│   ├── index.html
│   ├── signup.html
│   ├── login.html
│   ├── question1.html
│   ├── question2.html
│   ├── question3.html
│   ├── question4.html
│   └── learning_path.html
│
├── static/               # CSS files
│   ├── index.css
│   ├── signup.css
│   ├── question1.css
│   ├── question2.css
│   ├── question3.css
│   └── learning_path.css
│
└── README.md
```

---


Security Features

* Passwords are stored using **secure hashing**
* Input validation for **email and password**
* Session-based authentication



Future Improvements

* Integration with real AI/LLM models for better recommendations
* User progress tracking
* Resource ranking using machine learning
* Course bookmarking feature
* Dashboard for learning analytics


Author

Garnepally Varsha
