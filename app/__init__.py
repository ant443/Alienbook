from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models




# __init__.py - In Python, a sub-directory that includes a __init__.py file is considered a package, and can be imported. When you import a package, the __init__.py executes and defines what symbols the package exposes to the outside world.

# __name__ - a variable passed to the Flask class is a Python predefined variable, which is set to the name of the module in which it is used. Flask uses the location of the module passed here as a starting point when it needs to load associated resources
# In flask docs, it says if you are using a package, it's better for debugging to do this: app = Flask('microblog')

# two entities named app:
# The package itself(see __init__ description above), which is referenced in the from app import routes statement("The bottom import is a workaround to circular imports").
# The app variable which is an instance of the Flask class defined in __init__.py script making it a member of the app package.
# So one is the package, and the other is a variable(flask class instance).

# The script above simply creates the application object, as an instance of class Flask, imported from the flask package.
# config - again, lower case c config is the package, uppercase C is the actual class. 
# app.config.from_object(Config) - Load configurations from separate file(config), into app.config dictionary. "Then, in any of your files you could just import the app object to gain access to that dictionary."

# The database and migration engine instances needed to be created after the application(above stuff). The models module will define the structure of the database.