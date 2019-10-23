from flask import render_template, request, flash, redirect, url_for
from app import app
from datetime import datetime
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.route("/", methods=["POST", "GET"])
@app.route("/index", methods=["POST", "GET"])
def index():
    # user = {"username": "Miguel"}
    title = "Alienbook - log in or sign up"
    year = datetime.now().year
    form = LoginForm()
    # if request.method == "POST":
    #     print(request, flush=True)
    #     if form.validate_on_submit():
    #         flash(f"Login requested for user {form.email.data}")
    #         return redirect(url_for("index"))
    #     else:
    #         return redirect(url_for("login"))
    if current_user.is_anonymous:
        return render_template("index.html", title=title, year=year, form=form)
    else:
        return redirect(url_for("profile"))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = LoginForm()
    title = "Sign up for Alienbook | Alienbook"
    return render_template(
        "signup.html",
        title=title,
        hidden_menu=True,
        year=datetime.now().year,
        form=form,
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    # if request.method == "POST":
    #     print(request, flush=True)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return render_template(
                "login.html", title="Log in to Alienbook | Alienbook", form=form
            )
        login_user(user)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            flash(f"Login successful for user {form.email.data}")
            next_page = url_for("index")
        return redirect(next_page)
    return render_template(
        "login.html", title="Log in to Alienbook | Alienbook", form=form
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/confirm_email")
def confirm_email():
    return render_template("confirm_email.html")
