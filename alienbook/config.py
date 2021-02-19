import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).parent.resolve()
load_dotenv(basedir.joinpath(".env"))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "development_only_password" # TODO
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + str(basedir.joinpath("app.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir.joinpath("../images").resolve()
    LOGS = basedir.joinpath("../logs").resolve()
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024