from datetime import datetime, date
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    birthdate = db.Column(db.Date)
    gender = db.Column(db.String(8))
    username = db.Column(db.String(133), index=True, unique=True)
    posts = db.relationship("Post", back_populates="user", lazy="dynamic")
    photo = db.relationship(
        "Photo", 
        uselist=False, 
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
        )
    settings = db.relationship(
        "Settings", 
        uselist=False, 
        back_populates="user", 
        cascade="all, delete-orphan",
        passive_deletes=True
        )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_birthdate(self, day, month, year):
        date_format = "%d, %b, %Y"
        self.birthdate = datetime.strptime(f"{day}, {month}, {year}", date_format)

    def generate_username(self, username_pattern):
        def is_taken(username):
            if User.query.filter_by(username=username).first():
                return True

        def get_users(prefix):
            prefix = prefix.replace('/','//').replace('_', '/_').replace('%','/%')
            return User.query.filter(User.username.like(prefix + "%", escape='/')).all()

        def find_available_int(numeric_strings):
            i = 2
            while str(i) in numeric_strings:
                i += 1
            return i

        if not is_taken(username_pattern):
            self.username = username_pattern
            return
        username_pattern += "."
        users = get_users(username_pattern)
        prefix_length = len(username_pattern)
        username_suffixes = list(map(lambda x: x.username[prefix_length:], users))
        numeric_suffixes = list(filter(lambda x: x.isdigit(), username_suffixes))
        suffix = str(find_available_int(numeric_suffixes))
        self.username = username_pattern + suffix

    def __repr__(self):
        return f"<User {self.username}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post {self.body}>"


class Photo(db.Model):
    unsafe_name = db.Column(db.String(256))
    new_name = db.Column(db.String(40))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, 
        onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), 
        primary_key=True)
    user = db.relationship("User", back_populates="photo")

    def __repr__(self):
        return f"<Photo {self.new_name} of {self.user}>"

class Settings(db.Model):
    preserve_photo_data = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), 
        primary_key=True)
    user = db.relationship("User", back_populates="settings")

    def __repr__(self):
        return f"<Settings for {self.user}>"