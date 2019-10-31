from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    # remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    firstname = StringField("First name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("New password", validators=[DataRequired()])
    day = StringField("Day", validators=[DataRequired()])
    month = StringField("Month", validators=[DataRequired()])
    year = StringField("Year", validators=[DataRequired()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email address already in use.")
