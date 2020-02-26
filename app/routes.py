from app import app, db
from config import Config
from app.models import User

from flask import render_template, redirect, flash, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required

import os


@app.route("/", methods=["POST", "GET"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("login")
        password = request.form.get("password")

        user = User.query.filter_by(username = username).first()
        if user.check_password(password) is False:
            return redirect(url_for("index"))

        login_user(user)
        return redirect(url_for("register"))

    return render_template("index.html")



@app.route("/register", methods =["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    print('------ {0}'.format(request.form))


    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("password-confirmation")
        secret_key = request.form.get("secret-key")

        if password != confirm_password:
            print("mistake here")
            return redirect(url_for("register"))

        exists = User.query.filter_by(username = username).first()
        if exists is not None:
            print("error")
            flash("User by this name already exists")
            return redirect(url_for("register"))

        
        if (app.config['REGISTER_KEY']) != int(secret_key):
            print("incorrect secret_key")
            flash("incorrect secret_key")
            return redirect(url_for("register"))
        
        
        user = User(username = username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("register.html")
    


