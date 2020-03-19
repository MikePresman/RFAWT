from app import app, db
from config import Config
from app.models import User

from flask import render_template, redirect, flash, url_for, request, session, send_file
from flask_login import current_user, login_user, logout_user, login_required

from app.file_manager import walk_root_folder

from pathlib import Path
from ast import literal_eval as make_tuple
from shutil import copy
import os

@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method=="POST":
        send_file(request.values.get("download-link"), as_attachment=True)
    '''
    if current_user.is_authenticated is False:
        return redirect(url_for("index"))
    '''

    directory_info = walk_root_folder()    
    #user = User.query.filter_by(id=current_user.id).first()
    return render_template("home.html", name = "debug mode, put user.username after", info = directory_info)


@app.route("/download_file/<file_dir>", methods=["GET"])
def download_file(file_dir):
    return send_file(file_dir, as_attachment = True)

@app.route("/view_file/<file_dir>/<file_info>", methods=["GET"])
def view_file(file_dir, file_info):
    #check to make sure temp is clean, otherwise delete all exisiting files.
    directory = os.getcwd() + r'\app\static\img\temp'
    for root, dirs, files in os.walk(directory):
        for file in files:
            os.remove(directory + "\\" + file)
    
    #copy folder into temp folder since cant server static images from C:\ only from static folder
    new_dir = copy(file_dir, app.root_path + "/static/img/temp")
    _, file_type, extension, file_name = make_tuple(file_info)

    #check to make sure is viewable type
    if _ is False:
        return redirect(url_for('home'))

    return render_template("view.html", file_dir = "img/temp/" + file_name, file_type = file_type, extension = extension)

@app.route("/", methods=["POST", "GET"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember_me = request.form.get("remember-me")       
        remember_status = False

        user = User.query.filter_by(username = username).first()
        if user is None or user.check_password(password) is False:
            flash("Incorrect Login")
            return redirect(url_for("index"))
                
        remember_status = True if remember_me == "True" else False
        login_user(user, remember = remember_status)

        return redirect(url_for("home"))

    return render_template("index.html")

@app.route("/register", methods =["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

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
    



