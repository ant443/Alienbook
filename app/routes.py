from flask import render_template, request, flash, redirect, url_for
from app import app
from datetime import datetime


@app.route("/", methods=["POST", "GET"])
@app.route("/index", methods=["POST", "GET"])
def index():
    user = {"username": "Miguel"}
    title = "Alienbook - log in or sign up"
    year = year = datetime.now().year
    if request.method == "POST":
        if request.form["email"] == "admin" and request.form["password"] == "secret":
            print("here")
            flash("login successful, welcome user")
            return redirect(url_for("index"))
        else:
            return redirect(url_for("failedlogin"))

    return render_template(
        "index.html", title=title, user=user, year=year, particlejs=True
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template(
        "signup.html",
        title="Sign up for Alienbook | Alienbook",
        hidden_menu=True,
        year=datetime.now().year,
    )


@app.route("/failedlogin", methods=["POST", "GET"])
def failedlogin():
    return render_template("failed_login.html", title="Log in to Alienbook | Alienbook")


# decorators can be used to register the function that follows them as a callback for a certain event. When a web browser requests either of these two URLs "/" or "index", index will be called and it's return value will be passed back to the browser as a response.

# render_template - operation that converts a template into a complete HTML page.
# Jinja2 substitutes {{ ... }} blocks in the template, with the corresponding values, given by the arguments provided in the render_template() call.

# methods - tell flask which request methods should be accepted("GET" by default). POST requests should be used when the browser submits form data to the server.

# you can only have one extends tag called per rendering.
# make sure action attribute in form has the url you want(or url_for). empty string will send data to the form's URL.
# url_for can be used in place of link passing the name of the view function as it's parameter.
# make sure name attribute in form matches view functions form.request

