from app import app, db
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Post": Post}


# imports the app variable(the application instance) that is a member of the app package.
# If you find this confusing, you can rename either the package or the variable to something else.

# flask shell will pre-import app and anything else you wish to pre-import using the function above.
# Benefits include working with database entities without having to import them.

