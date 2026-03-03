from flask import Flask, render_template, request, redirect, session
from mongodb import users_collection
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
from ai_engine import generate_learning_path

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')



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



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        password = (request.form.get("password") or "").strip()
        domain = (request.form.get("domain") or "").strip()

        if not name or not email or not password or not domain:
            return "All fields are required!"

        if not is_valid_email(email):
            return "Invalid email format!"

        if not is_strong_password(password):
            return "Password must be at least 8 characters with uppercase, lowercase and number."

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




@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        password = (request.form.get("password") or "").strip()

        if not email or not password:
            return "Please enter email and password."

        user = users_collection.find_one({"email": email})

        if not user:
            return "Email not registered."

        if not check_password_hash(user["password"], password):
            return "Incorrect password."

        session["email"] = email
        session["name"] = user["name"]

        if user.get("level"):
            return redirect("/generate-path")
        else:
            return redirect("/question2")

    return render_template("login.html")



@app.route("/question2", methods=["GET", "POST"])
def question2():
    if "email" not in session:
        return redirect("/login")


    users_collection.update_one(
        {"email": session["email"]},
        {
            "$unset": {
                "learning_path": "",
                "completed_courses": "",
                "level": "",
                "preference": ""
            }
        }
    )

    if request.method == "POST":
        pref = request.form.get("preference", "")
        session["preference"] = pref.lower() if pref else ""
        return redirect("/question3")

    return render_template("question2.html")



@app.route("/question3", methods=["GET", "POST"])
def question3():
    if "email" not in session:
        return redirect("/login")

    if request.method == "POST":
        session["time"] = request.form.get("time")
        return redirect("/question4")

    return render_template("question3.html")



@app.route("/question4", methods=["GET", "POST"])
def question4():
    if "email" not in session:
        return redirect("/login")

    if request.method == "POST":
        level = request.form.get("level")

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




@app.route("/generate-path")
def generate_path():

    if "email" not in session:
        return redirect("/login")

    user = users_collection.find_one({"email": session["email"]})

    if not user:
        return "User not found"

    required_fields = ["domain", "preference", "level"]
    missing_fields = [f for f in required_fields if f not in user]

    if missing_fields:
        return redirect("/question2")

    try:
        materials = generate_learning_path(user)


        users_collection.update_one(
            {"email": session["email"]},
            {
                "$set": {
                    "learning_path": [str(m["_id"]) for m in materials]
                }
            }
        )

        user = users_collection.find_one({"email": session["email"]})

        learning_path = user.get("learning_path", [])
        completed = user.get("completed_courses", [])

        total = len(learning_path)
        done = len(completed)

        percentage = int((done / total) * 100) if total > 0 else 0

        return render_template(
    "learning_path.html",
    courses=materials,
    progress=percentage,
    completed_all=(percentage == 100)
)

    except Exception as e:
        return f"Error generating learning path: {str(e)}"



@app.route("/complete/<course_id>")
def complete_course(course_id):

    if "email" not in session:
        return redirect("/login")

    users_collection.update_one(
        {"email": session["email"]},
        {"$addToSet": {"completed_courses": course_id}}
    )

    return redirect("/generate-path")




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)