from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'bank_secret'
accounts = {}

@app.route("/")
def home():
    return render_template("home.html", title="Home")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        pin = request.form["pin"]
        if username in accounts:
            return "Account already exists!"
        accounts[username] = {"pin": pin, "balance": 0}
        return redirect("/login")
    return render_template("register.html", title="Register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        pin = request.form["pin"]
        if username in accounts and accounts[username]["pin"] == pin:
            session["user"] = username
            return redirect("/dashboard")
        return "Invalid credentials!"
    return render_template("login.html", title="Login")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user" not in session:
        return redirect("/login")
    user = session["user"]
    balance = accounts[user]["balance"]
    return render_template("dashboard.html", username=user, balance=balance, title="Dashboard")

@app.route("/deposit", methods=["POST"])
def deposit():
    if "user" in session:
        user = session["user"]
        amount = float(request.form["amount"])
        accounts[user]["balance"] += amount
    return redirect("/dashboard")

@app.route("/withdraw", methods=["POST"])
def withdraw():
    if "user" in session:
        user = session["user"]
        amount = float(request.form["amount"])
        if accounts[user]["balance"] >= amount:
            accounts[user]["balance"] -= amount
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
