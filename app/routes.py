from flask import render_template, request, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.route("/", methods=["POST", "GET"])
def index():
    title = "Alienbook - log in or sign up"
    login_form = LoginForm()
    signup_form = RegistrationForm()
    users = User.query.all()
    print(list(map(lambda x: x.email, users)), flush=True)
    if current_user.is_anonymous:
        return render_template(
            "index.html",
            title=title,
            login_form=login_form,
            signup_form=signup_form,
            logo_heading=True,
        )
    else:
        return render_template("user_index.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    login_form = LoginForm()
    signup_form = RegistrationForm()
    title = "Sign up for Alienbook | Alienbook"
    if signup_form.validate_on_submit():
        user = User(
            firstname=signup_form.firstname.data,
            surname=signup_form.surname.data,
            email=signup_form.email.data.lower(),
            gender=signup_form.gender.data,
        )
        user.set_password(signup_form.password.data)
        user.set_birthdate(
            signup_form.day.data, signup_form.month.data, signup_form.year.data
        )
        username_pattern = signup_form.firstname.data + "." + signup_form.surname.data
        user.generate_username(username_pattern)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))

    return render_template(
        "signup.html",
        title=title,
        hidden_menu=True,
        login_form=login_form,
        signup_form=signup_form,
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash("Invalid username or password")
            return render_template(
                "login.html",
                title="Log in to Alienbook | Alienbook",
                login_form=login_form,
            )
        login_user(user)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            flash(f"Login successful for user {login_form.email.data}")
            next_page = url_for("index")
        return redirect(next_page)
    return render_template(
        "login.html", title="Log in to Alienbook | Alienbook", login_form=login_form
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {"author": user, "body": "Test post #1"},
        {"author": user, "body": "Test post #2"},
    ]
    return render_template("profile.html", user=user, posts=posts)


@app.route("/confirm_email")
def confirm_email():
    return render_template("confirm_email.html", title="Alienbook")


@app.route("/help/delete_account")
@login_required
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    return redirect("/logout")
