from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Enable foreign key support in sqlite #
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
# End 'Enable foreign key support in sqlite' block #

app = Flask(__name__)
app.config.from_object(Config)
app.config["LOGS"].mkdir(exist_ok=True)
scheduled_delete = app.config["UPLOAD_FOLDER"].joinpath("scheduled_delete")
scheduled_delete.mkdir(parents=True, exist_ok=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"

from app import routes, models
