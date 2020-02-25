from flask import render_template, request, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


def signup_user(signup_form):
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


@app.route("/", methods=["POST", "GET"])
def index():
    title = "Alienbook - log in or sign up"
    login_form = LoginForm()
    signup_form = RegistrationForm()
    # testing #
    users = User.query.all()
    print("Users list: ", list(map(lambda x: x.email, users)), flush=True)
    # endblock testing #
    if current_user.is_anonymous:
        return render_template(
            "index.html",
            title=title,
            login_form=login_form,
            signup_form=signup_form,
            logo_heading=True,
        )
    else:
        return render_template("user_index.html", title="Alienbook")


@app.route("/signup/AJAX", methods=["POST"])
@app.route("/signup/", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    login_form = LoginForm()
    signup_form = RegistrationForm()
    title = "Sign up for Alienbook | Alienbook"
    data_is_valid = signup_form.validate_on_submit()
    if request.path == "/signup/AJAX":
        for el in signup_form:
            if el.errors:
                return str(el.errors[0])
        signup_user(signup_form)
        flash("Congratulations, you are now a registered user!")
        return ""
    if data_is_valid:
        signup_user(signup_form)
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
    def get_next_page(request, view_name):
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for(view_name)
        return next_page

    if current_user.is_authenticated:
        return redirect(url_for("index"))
    login_form = LoginForm()
    url = "login.html"
    template_variables = {
        "title": "Log in to Alienbook | Alienbook",
        "login_form": login_form,
    }
    if request.method == "GET":
        return render_template(url, **template_variables)
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is None:
            login_form.email.errors.append("email not found.")
            return render_template(url, **template_variables)
        if not user.check_password(login_form.password.data):
            login_form.password.errors.append("incorrect password.")
            return render_template(url, **template_variables)
        login_user(user)
        flash(f"Login successful for user {login_form.email.data}")
        return redirect(get_next_page(request, "index"))
    return render_template(url, **template_variables)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    title = f"{user.firstname} {user.surname}"
    posts = [
        {"author": user, "body": "Test post #1"},
        {"author": user, "body": "Test post #2"},
    ]
    return render_template("profile.html", user=user, title=title, posts=posts)


@app.route("/confirm_email")
def confirm_email():
    return render_template("confirm_email.html", title="Alienbook")


@app.route("/help/delete_account")
@login_required
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    return redirect("/logout")
