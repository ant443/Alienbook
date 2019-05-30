from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    # return "Hello, World!"
    user = {"username": "Miguel"}
    # posts = [
    #   {
    #     "author": {"username": "John"},
    #     "body": "Beautiful day in Portland!"
    #   },
    #   {
    #     "author": {"username": "Susan"},
    #     "body": "The Avengers movie was so cool!"
    #   }
    # ]
    return render_template("index.html", title="Facebook - log in or sign up", user=user)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    return render_template("signup.html", title="Sign up to Facebook | Facebook", hidden_menu=True)

# if bad login, go to failed login page, title="Log in to Facebook | Facebook"

# decorators can be used to register the function that follows them as a callback for a certain event. When a web browser requests either of these two URLs "/" or "index", index will be called and it's return value will be passed back to the browser as a response.

# render_template - operation that converts a template into a complete HTML page.
# Jinja2 substitutes {{ ... }} blocks in the template, with the corresponding values, given by the arguments provided in the render_template() call.

# methods - tell flask which request methods should be accepted("GET" by default). POST requests should be used when the browser submits form data to the server.



