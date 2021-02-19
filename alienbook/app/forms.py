import unicodedata

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    RadioField,
    HiddenField
)
from wtforms.validators import DataRequired, Email, ValidationError, Length
from app.models import User
from calendar import month_abbr
from datetime import datetime

def normalize_str(self, field):
    "normalize before checking filename length"
    field.data = unicodedata.normalize("NFC", field.data)

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), normalize_str])
    submit = SubmitField("Log In")

class RegistrationForm(FlaskForm):

    def day_choices():
        days = []
        days.append(("", "Day"))
        for day_num in range(1, 32):
            day_num = str(day_num)
            days.append((day_num, day_num))
        return days

    def month_choices():
        months = []
        months.append(("", "Month"))
        for month in month_abbr[1:]:
            months.append((month, month))
        return months

    def year_choices():
        this_year = datetime.now().year
        years = []
        max_years = 120
        years.append(("", "Year"))
        for year in range(this_year, this_year - (max_years + 1), -1):
            year = str(year)
            years.append((year, year))
        return years

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user is not None:
            raise ValidationError("Email address already in use.")

    def validate_day(self, day):
        def years_old(birthdate, date_today):
            years_old = date_today.year - int(birthdate.year)
            if (date_today.month < birthdate.month) or (
                (birthdate.month == date_today.month) and date_today.day < birthdate.day
            ):
                years_old -= 1
            return years_old

        day = day.data
        month = self.month.data
        year = self.year.data
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
            raise ValidationError("You are not old enough.")
        if max_years < user_years:
            raise ValidationError("No one is that old yet.")

    firstname = StringField("First name", validators=[DataRequired(), 
        normalize_str, Length(max=64)])
    surname = StringField("Surname", validators=[DataRequired(), normalize_str, 
        Length(max=64)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("New password", validators=[DataRequired(), normalize_str, 
        Length(min=8, message="Passwords should be at least 8 characters in "
            "length. We recommend an unusual phrase or sentence")])
    day = SelectField("Day", validators=[DataRequired()], choices=day_choices())
    month = SelectField("Month", validators=[DataRequired()], choices=month_choices())
    year = SelectField("Year", validators=[DataRequired()], choices=year_choices())
    gender = RadioField(
        "Gender",
        validators=[DataRequired()],
        choices=[("Female", "Female"), ("Male", "Male")],
    )

def normalize_photo_str(self, photo):
    "normalize before checking filename length"
    photo.data.filename = unicodedata.normalize("NFC", photo.data.filename)
    
class PhotoForm(FlaskForm):
    def validate_photo(self, photo):
        if len(photo.data.filename) > 256:
            raise ValidationError("filename too long. Keep it under 256 "
                "characters please.")

    photo = FileField("photo", validators=[
        FileRequired(),
        FileAllowed(["jpg", "jpeg", "png"], 
                    "file type not allowed."),
        normalize_photo_str
        ])
    submitbtn = SubmitField("Upload")
    
class DeletePhotoForm(FlaskForm):
    deletebtn = SubmitField("Remove photo")

class DeleteAccountForm(FlaskForm):
    delete_acc = SubmitField("Delete Account")
    form_identifier = HiddenField()

class SettingsForm(FlaskForm):
    photo_metadata = BooleanField("Preserve metadata in profile picture")
    settings_submit = SubmitField("Save Changes")