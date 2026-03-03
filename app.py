from flask import Flask, render_template, request, redirect, session
from mongodb import users_collection
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
from ai_engine import generate_learning_path

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')





# -------------------- VALIDATION FUNCTIONS --------------------

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True
# -------------------- HOME --------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------- SIGNUP --------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        # Get all form data
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        domain = request.form.get("domain")

        # Add .strip() safely
        name = (name or "").strip()
        email = (email or "").strip()
        password = (password or "").strip()
        domain = (domain or "").strip()

        # Validate empty fields
        if not name or not email or not password or not domain:
            return "All fields are required!"

        # Validate email format
        if not is_valid_email(email):
            return "Invalid email format!"

        # Validate password strength
        if not is_strong_password(password):
            return "Password must be at least 8 characters with uppercase, lowercase and number."

        # Check if user already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return "User already exists! Please login."

        hashed_password = generate_password_hash(password)

        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password,
            "domain": domain
        })

        session["email"] = email
        session["name"] = name
        session["domain"] = domain

        return redirect("/question2")

    return render_template("signup.html")

# -------------------- LOGIN --------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()

        if not email or not password:
            return "Please enter email and password."

        user = users_collection.find_one({"email": email})

        if not user:
            return "Email not registered."

        if not check_password_hash(user["password"], password):
            return "Incorrect password."

        session["email"] = email
        session["name"] = user["name"]

        # 🔥 Check if user has completed questionnaire
        if user.get("level"):
            return redirect("/generate-path")
        else:
            return redirect("/question2")

    return render_template("login.html")


# -------------------- QUESTION 2 --------------------
@app.route("/question2", methods=["GET", "POST"])
def question2():
    if "email" not in session:
        return redirect("/login")

    if request.method == "POST":
        pref = request.form.get("preference", "")
        session["preference"] = pref.lower() if pref else ""
        return redirect("/question3")

    return render_template("question2.html")


# -------------------- QUESTION 3 --------------------
@app.route("/question3", methods=["GET", "POST"])
def question3():
    if "email" not in session:
        return redirect("/login")

    if request.method == "POST":
        session["time"] = request.form.get("time")
        return redirect("/question4")

    return render_template("question3.html")


# -------------------- QUESTION 4 --------------------
@app.route("/question4", methods=["GET", "POST"])
def question4():
    if "email" not in session:
        return redirect("/login")

    if request.method == "POST":
        level = request.form.get("level")

        # Update user document with all onboarding data
        users_collection.update_one(
            {"email": session["email"]},
            {
                "$set": {
                    "preference": session.get("preference"),
                    "level": level
                }
            }
        )

        return redirect("/generate-path")

    return render_template("question4.html")

# -------------------- TEST ROUTE --------------------
@app.route("/test")
def test():
    users_collection.insert_one({"test": "working"})
    return "Inserted Test Data"

@app.route("/generate-path")
def generate_path():

    if "email" not in session:
        return redirect("/login")

    user = users_collection.find_one({"email": session["email"]})

    if not user:
        return "User not found"

    # ✅ Check for correct required fields
    required_fields = ["domain", "preference", "level"]
    missing_fields = [f for f in required_fields if f not in user]

    if missing_fields:
        return redirect("/question2")

    try:
        materials = generate_learning_path(user)

        print("Generated Materials:", materials)

        if not materials:
            return render_template(
                "learning_path.html",
                courses=[],
                message="No courses found matching your preferences."
            )

        return render_template("learning_path.html", courses=materials)

    except Exception as e:
        return f"Error generating learning path: {str(e)}"

if __name__ == "__main__":
    app.run(debug=False)