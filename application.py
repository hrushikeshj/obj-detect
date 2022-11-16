from flask import Flask, flash, render_template, request, Response, redirect, url_for, session
from flask_bootstrap import Bootstrap
from models import User
from database import db_session

from object_detection import *
from camera_settings import *


application = Flask(__name__)
Bootstrap(application)
application.secret_key = 'qwert23456##\l'

check_settings()
VIDEO = VideoStreaming()


@application.route("/sign_up")
def signup():
    return render_template("sign_up.html")

@application.route("/user", methods=['post'])
def create_user():
    data = request.form
    e_user = User.query.filter(User.email == data["email"]).first()
    if e_user is not None:
        flash("Email is already taken!", 'danger')
        return redirect(url_for('signup'))

    
    user = User(**data)
    db_session.add(user)
    db_session.commit()
    flash("Accout created", 'success')
    return redirect(url_for('login'))


@application.route("/login")
def login():
    return render_template("login.html")


@application.route("/session", methods=['post'])
def create_session():
    data = request.form
    e_user = User.query.filter(User.email == data["email"]).first()
    if e_user is None:
        flash("User not found", 'danger')
        return redirect(url_for('login'))
    
    if e_user.val(data["password"]) == False:
        flash("Wrong passwoed", 'danger')
        return redirect(url_for('login'))

    session["username"] = e_user.name
    flash("Logged in!!", 'success')
    return redirect(url_for('home'))


@application.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out!!", 'success')
    return redirect(url_for('login'))


@application.route("/")
def home():
    if "username" not in session:
        flash("Login to detect objects", 'danger')
        return redirect(url_for('login'))
    TITLE = "Object detection"
    return render_template("index.html", TITLE=TITLE)


@application.route("/video_feed")
def video_feed():
    """
    Video streaming route.
    """
    return Response(
        VIDEO.show(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@application.route("/obj_dect")
def obj_dect_json():
    j = VIDEO.show_dict()
    #print(j)
    return {'ans': j}


# * Button requests
@application.route("/request_preview_switch")
def request_preview_switch():
    VIDEO.preview = not VIDEO.preview
    print("*"*10, VIDEO.preview)
    return "nothing"


@application.route("/request_flipH_switch")
def request_flipH_switch():
    VIDEO.flipH = not VIDEO.flipH
    print("*"*10, VIDEO.flipH)
    return "nothing"


@application.route("/request_model_switch")
def request_model_switch():
    VIDEO.detect = not VIDEO.detect
    print("*"*10, VIDEO.detect)
    return "nothing"


@application.route("/request_exposure_down")
def request_exposure_down():
    VIDEO.exposure -= 1
    print("*"*10, VIDEO.exposure)
    return "nothing"


@application.route("/request_exposure_up")
def request_exposure_up():
    VIDEO.exposure += 1
    print("*"*10, VIDEO.exposure)
    return "nothing"


@application.route("/request_contrast_down")
def request_contrast_down():
    VIDEO.contrast -= 4
    print("*"*10, VIDEO.contrast)
    return "nothing"


@application.route("/request_contrast_up")
def request_contrast_up():
    VIDEO.contrast += 4
    print("*"*10, VIDEO.contrast)
    return "nothing"


@application.route("/reset_camera")
def reset_camera():
    STATUS = reset_settings()
    print("*"*10, STATUS)
    return "nothing"


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')
