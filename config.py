import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "nothing-to-see-here"


# SECRET_KEY - Flask and some of its extensions use it's value as a cryptographic key, useful to generate signatures or tokens.
# The Flask-WTF extension uses it to protect web forms against Cross-Site Request Forgery or CSRF (pronounced "seasurf").