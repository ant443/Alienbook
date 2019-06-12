import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "nothing-to-see-here"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# SECRET_KEY - Flask and some of its extensions use it's value as a cryptographic key, useful to generate signatures or tokens.
# The Flask-WTF extension uses it to protect web forms against Cross-Site Request Forgery or CSRF (pronounced "seasurf").

# SQLALCHEMY stuff - basdir is the absolute path of our project
# ..URI tries to find database url, and we provided it a fallback which is to configure a database named app.db.
# track_modifications - signals the application every time a change is about to be made in the database. we dont need it.