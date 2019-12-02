from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    RadioField,
)
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User
from calendar import month_abbr
from datetime import datetime


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    # remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    def day_choices():
        days = []
        days.append(("0", "Day"))
        for day_num in range(1, 32):
            day_num = str(day_num)
            days.append((day_num, day_num))
        return days

    def month_choices():
        months = []
        months.append(("0", "Month"))
        for month in month_abbr[1:]:
            months.append((month, month))
        return months

    def year_choices():
        this_year = datetime.now().year
        years = []
        max_years = 120
        years.append(("0", "Year"))
        for year in range(this_year, this_year - (max_years + 1), -1):
            year = str(year)
            years.append((year, year))
        return years

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user is not None:
            raise ValidationError("Email address already in use.")

    def validate_date(self, day, month, year):
        def years_old(birthdate, date_today):
            years_old = date_today.year - int(birthdate.year)
            if (date_today.month < birthdate.month) or (
                (birthdate.month == date_today.month) and date_today.day < birthdate.day
            ):
                years_old -= 1
            return years_old

        date_today = datetime.today()
        date_format = "%d, %b, %Y"
        min_years = 13
        max_years = 120
        try:
            birthdate = datetime.strptime(f"{day}, {month}, {year}", date_format)
        except:
            raise ValidationError("Not a valid date.")

        user_years = years_old(birthdate, date_today)
        if user_years < min_years:
            raise ValidationError("You are not old enough")
        if max_years < user_years:
            raise ValidationError("No one is that old yet")

    firstname = StringField("First name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("New password", validators=[DataRequired()])
    day = SelectField("Day", validators=[DataRequired()], choices=day_choices())
    month = SelectField("Month", validators=[DataRequired()], choices=month_choices())
    year = SelectField("Year", validators=[DataRequired()], choices=year_choices())
    gender = RadioField(
        "Gender",
        validators=[DataRequired()],
        choices=[("Female", "Female"), ("Male", "Male")],
    )

