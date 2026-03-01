from flask import Flask, render_template, request, redirect

app = Flask(__name__)

user_data = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_data["name"] = request.form.get("name")
        user_data["email"] = request.form.get("email")
        user_data["password"] = request.form.get("password")
        return redirect("/question1")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/question1")
    return render_template("login.html")

@app.route("/question1", methods=["GET", "POST"])
def question1():
    if request.method == "POST":
        user_data["goal"] = request.form.get("goal")
        return redirect("/question2")
    return render_template("question1.html")

@app.route("/question2", methods=["GET", "POST"])
def question2():
    if request.method == "POST":
        user_data["preference"] = request.form.get("preference")
        return redirect("/question3")
    return render_template("question2.html")

@app.route("/question3", methods=["GET", "POST"])
def question3():
    if request.method == "POST":
        user_data["time"] = request.form.get("time")
        print("User Data:", user_data)
        return redirect("/question4")
    return render_template("question3.html")

@app.route("/question4", methods=["GET", "POST"])
def question4():
    if request.method == "POST":
        user_data["level"] = request.form.get("level")
        print("Final User Data:", user_data)
        return "Setup Complete! Profile Created Successfully."
    return render_template("question4.html")

if __name__ == "__main__":
    app.run(debug=False)