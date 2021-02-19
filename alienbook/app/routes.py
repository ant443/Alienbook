import uuid
import warnings
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import time

from PIL import Image, UnidentifiedImageError
from flask import (render_template, request, flash, redirect, url_for, 
    send_from_directory, abort)
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

from app import app, db
from app.forms import (LoginForm, RegistrationForm, PhotoForm, DeletePhotoForm, 
    DeleteAccountForm, SettingsForm)
from app.models import User, Photo, Settings, Post

photo_logger = logging.getLogger('photo')
photo_logger.setLevel(logging.WARNING)
formatter1 = logging.Formatter("[%(asctime)s] %(levelname)s in %(name)s: %(message)s")
photo_handler = RotatingFileHandler(
    app.config["LOGS"].joinpath("photo.log"),
    maxBytes = 1024 * 1024,
    backupCount = 5
    )
photo_handler.setFormatter(formatter1)
photo_logger.addHandler(photo_handler)

Image.warnings.simplefilter('error', Image.DecompressionBombWarning)

delete_account_logger = logging.getLogger('del_account')
delete_account_logger.setLevel(logging.WARNING)
formatter2 = logging.Formatter("[%(asctime)s] %(levelname)s in %(name)s: %(message)s")
delete_account_handler = RotatingFileHandler(
    app.config["LOGS"].joinpath("del_acc.log"),
    maxBytes = 1024 * 1024,
    backupCount = 5
    )
delete_account_handler.setFormatter(formatter2)
delete_account_logger.addHandler(delete_account_handler)

general_logger = logging.getLogger('general')
general_logger.setLevel(logging.WARNING)
general_logger_handler = RotatingFileHandler(
    app.config["LOGS"].joinpath("general.log"),
    maxBytes = 1024 * 1024,
    backupCount = 10
    )
general_logger_handler.setFormatter(formatter2)
general_logger.addHandler(general_logger_handler)

def signup_user(signup_form):
    user = User(
        firstname = signup_form.firstname.data,
        surname = signup_form.surname.data,
        email = signup_form.email.data.lower(),
        gender = signup_form.gender.data,
    )
    user.set_password(signup_form.password.data)
    user.set_birthdate(
        signup_form.day.data, signup_form.month.data, signup_form.year.data
    )
    username_pattern = signup_form.firstname.data + "." + signup_form.surname.data
    user.generate_username(username_pattern)
    db.session.add(user)
    db.session.commit()
    try:
        Path(app.config["UPLOAD_FOLDER"], str(user.id), "profile").mkdir(parents=True)
    except FileExistsError as e:
        general_logger.error(f"{user.id} id folder already existed when account "
        f"created for {user.email}. {e}")
    except Exception as e:
        general_logger.error(f"{e} happened for user id: {user.id} and email: "
        f"{user.email}")
    settings = Settings(user_id=user.id)
    db.session.add(settings)
    db.session.commit()

@app.route("/", methods=["POST", "GET"])
def index():
    title = "Alienbook - log in or sign up"
    login_form = LoginForm()
    signup_form = RegistrationForm()
    if current_user.is_anonymous:
        return render_template(
            "index.html",
            title=title,
            login_form=login_form,
            signup_form=signup_form,
        )
    else:
        return render_template("user_index.html", title="Alienbook")

@app.route("/signup/AJAX", methods=["POST"])
@app.route("/signup/", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    login_form = LoginForm()
    signup_form = RegistrationForm()
    title = "Sign up for Alienbook | Alienbook"
    data_is_valid = signup_form.validate_on_submit()
    if request.path == "/signup/AJAX":
        for el in signup_form:
            if el.errors:
                return str(el.errors[0])
        try:
            signup_user(signup_form)
        except Exception as e:
            general_logger.error(f"Problem creating account for "
            f"{signup_form.firstname.data} {signup_form.surname.data} {e}")
            return "An unexpected error occured. Please try again, or contact support."
        flash("Congratulations, you are now a registered user!", "info")
        return ""
    if data_is_valid:
        try:
            signup_user(signup_form)
            flash("Congratulations, you are now a registered user!", "info")
            return redirect(url_for("login"))
        except Exception as e:
            general_logger.error(f"Problem creating account for "
            f"{signup_form.firstname.data} {signup_form.surname.data} {e}")
            flash("An unexpected error occured. Please try again, or contact support.")
    return render_template(
        "signup.html",
        title=title,
        hidden_menu=True,
        login_form=login_form,
        signup_form=signup_form,
    )

@app.route("/login", methods=["POST", "GET"])
def login():
    def get_next_page(request, view_name):
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for(view_name)
        return next_page

    if current_user.is_authenticated:
        return redirect(url_for("index"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data.lower()).first()
        if user is None:
            login_form.email.errors.append("email not found.")
        elif not user.check_password(login_form.password.data):
            login_form.password.errors.append("incorrect password.")
        else:
            login_user(user)
            return redirect(get_next_page(request, "index"))
    return render_template(
        "login.html", 
        title="Log in to Alienbook | Alienbook",
        login_form=login_form,
    )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

def delete_all_profile_images_else_log_path(profile_path):
    """ Delete all images in user_id's profile folder."""
    EXTENSIONS = {".png", ".jpg", ".jpeg"}
    for p in profile_path.glob("*"):
        if p.suffix in EXTENSIONS:
            try:
                p.unlink()
            except:
                photo_logger.error(f"problem deleting image with path: {p}")

def delete_id_folder_else_log_path(user_id: str):
    scheduled_dir = app.config["UPLOAD_FOLDER"].joinpath("scheduled_delete")
    # match "user_id date" pattern in filenames:
    for id_dir in scheduled_dir.glob(f"{user_id} *"):
        profile_path = id_dir.joinpath("profile")
        delete_all_profile_images_else_log_path(profile_path)
        try:
            profile_path.rmdir()
            id_dir.rmdir()
        except Exception as e:
            photo_logger.error(f"problem removing id folder for {id_dir} {e}")

def delete_images_starting_with_name_else_log_path(user_id: str, name: str):
    """Typical use: delete uuid named files ignoring extension."""
    profile_path = app.config["UPLOAD_FOLDER"].joinpath(
    user_id,
    "profile"
    )
    for p in profile_path.glob(f"{name}*"):
        try:
            p.unlink()
        except:
            photo_logger.error(f"problem deleting image with path: {p}")

def save_and_resize(photo_form, user_id: str, preserve_metadata: bool):
    f = photo_form.photo.data
    new_uuid = uuid.uuid4().hex
    ext = f.filename.rpartition(".")[-1].lower()
    new_name = f"{new_uuid}.{ext}"
    profile_path = app.config["UPLOAD_FOLDER"].joinpath(
        user_id,
        "profile"
        )
    image_path = profile_path.joinpath(new_name)
    try:
        f.save(str(image_path))
        with Image.open(image_path) as im:
            if ext in ["jpg", "jpeg"] and im.mode != "RGB":
                im = im.convert("RGB")
            exif = {}
            if preserve_metadata:
                exif_data = im.info.get("exif")
                if exif_data:
                    exif = {"exif": exif_data}
            # icon
            small = im.resize((24,24), Image.LANCZOS)
            small_path = profile_path.joinpath(f"{new_uuid}-small.{ext}")
            small.save(small_path, optimize=True, quality=85, **exif)
            # posts image
            medium = im.resize((40,40), Image.LANCZOS)
            medium_path = profile_path.joinpath(f"{new_uuid}-medium.{ext}")
            medium.save(medium_path, optimize=True, quality=85, **exif)
            # profile image(overwrites original)
            im = im.resize((160,160), Image.LANCZOS)
            im.save(image_path, optimize=True, quality=85, **exif)
        existing_photo = Photo.query.filter_by(user_id=int(user_id)).first()
        if existing_photo:
            old_uuid = existing_photo.new_name.rpartition(".")[0]
            existing_photo.unsafe_name = f.filename
            existing_photo.new_name = new_name
            db.session.commit()
            delete_images_starting_with_name_else_log_path(user_id, old_uuid)
        else:
            photo = Photo(
                unsafe_name = f.filename,
                new_name = new_name,
                user_id = int(user_id)
            )
            db.session.add(photo)
            db.session.commit()
    # delete uploaded photo & resized versions, and inform user of problem.
    except UnidentifiedImageError:
        photo_logger.error(f"UnidentifiedImageError for user: {user_id}")
        delete_images_starting_with_name_else_log_path(user_id, new_uuid)
        photo_form.photo.errors.append(
            "An image could not be located in that file."
            )
    except (Image.DecompressionBombError, Image.DecompressionBombWarning):
        photo_logger.error(f"DecompressionBombWarning for user: {user_id}")
        delete_images_starting_with_name_else_log_path(user_id, new_uuid)
        photo_form.photo.errors.append(
            "Image contains too many pixels. "
            "Please resize it and try again."
            )
    except Exception:
        photo_logger.exception(f"profile image error for user: {user_id}")
        delete_images_starting_with_name_else_log_path(user_id, new_uuid)
        photo_form.photo.errors.append(
            "An unexpected error occured. Please try again, "
            "or contact support."
            )

@app.route("/profile/<path:username>", methods=("GET", "POST"))
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    profile_id = str(user.id)
    title = f"{user.firstname} {user.surname}".title()
    posts = [
        {"user": user, "body": "Test post #1"},
        {"user": user, "body": "Test post #2"},
    ]
    is_profile_of_user = current_user == user
    photo_form = PhotoForm()
    delete_photo_form = DeletePhotoForm()
    if delete_photo_form.deletebtn.data and delete_photo_form.validate_on_submit():
        user_id = str(current_user.id)
        existing_photo = Photo.query.filter_by(user_id=int(user_id)).first()
        if existing_photo:
            try:
                db.session.delete(existing_photo)
                db.session.commit()
            except Exception:
                photo_logger.exception(f"Delete photo error for user: {user_id}")
                flash("An unexpected error occured. Please try again, "
                    "or contact support.")
            profile_path = app.config["UPLOAD_FOLDER"].joinpath(
                user_id,
                "profile"
                )
            delete_all_profile_images_else_log_path(profile_path)
    if not delete_photo_form.deletebtn.data and photo_form.validate_on_submit(): 
        user_id = str(current_user.id)
        preserve_metadata = current_user.settings.preserve_photo_data
        save_and_resize(photo_form, user_id, preserve_metadata)
    return render_template(
        "profile.html",
        user=user,
        title=title,
        posts=posts,
        is_profile_of_user=is_profile_of_user,
        photo_form=photo_form,
        delete_photo_form=delete_photo_form,
        profile_id=profile_id
    )

@app.route("/uploads/<int:folder_name>/<path:filename>")
def download_file(filename, folder_name):
    directory = app.config["UPLOAD_FOLDER"].joinpath(
        str(folder_name),
        "profile"
        )
    return send_from_directory(directory, filename)

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    del_account_form = DeleteAccountForm()
    settings_form = SettingsForm()
    saved=""
    if del_account_form.form_identifier.data and del_account_form.validate_on_submit():
        try:
            user_folder = app.config["UPLOAD_FOLDER"].joinpath(str(current_user.id))
            if user_folder.is_dir():
                target_path = app.config["UPLOAD_FOLDER"].joinpath(
                    "scheduled_delete",
                    f"{current_user.id} {int(time.time())}"
                    )
                user_folder.rename(target_path)
            db.session.delete(current_user)
            db.session.commit()
            try:
                delete_id_folder_else_log_path(str(current_user.id))
            except Exception as e:
                delete_account_logger.exception(
                    f"Delete folder error for user: {current_user.id} {e}"
                    )
            return redirect(url_for("logout"))
        except Exception as e:
            delete_account_logger.exception(f"Delete account error for user: "
            f"{current_user.id} {e}")
            flash("An unexpected error occured. Please try again, or contact support.")
    if settings_form.settings_submit.data and settings_form.validate_on_submit():
        current_user.settings.preserve_photo_data = settings_form.photo_metadata.data
        try:
            db.session.commit()
            saved="1"
        except Exception as e:
            flash("An unexpected error occured. Please try again, or contact support.")
            general_logger.error(f"Problem changing settings for {current_user.id} {e}")
    return render_template(
        'settings.html',
        delete_account_form=del_account_form,
        settings_form=settings_form,
        title="Alienbook",
        saved=saved
        )

@app.route("/confirm_email")
def confirm_email():
    return render_template("confirm_email.html", title="Alienbook")