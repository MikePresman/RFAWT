from flask import render_template, redirect, flash, url_for, request, session, send_file, jsonify
from flask_login import current_user, login_user, logout_user, login_required
import socket
from app import app, db
from config import Config
from app.models import User, LocalNetwork
from app.file_manager import walk_root_folder, walk_folder
import requests
import json
import zlib
import sys
from datetime import datetime
from ast import literal_eval as make_tuple
from shutil import copy
import os
import pickle
import ast
import base64
from config import Config


class LoggedInUser():
    def __init__(self, id):
        self.user_id = id
        self.username = User.query.filter_by(id = id).first().username


@app.route("/", methods=["POST", "GET"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

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
        global user_logged_in
        user_logged_in = LoggedInUser(current_user.id)

        return redirect(url_for("dashboard"))

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

@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    pcs_on_network = LocalNetwork.query.all()
    return render_template("dashboard.html", name = user_logged_in.username, pcs = pcs_on_network)

@app.route("/pc-access/<pc_name>/<folder>", methods = ["GET"])
@login_required
def pc_access(pc_name, folder):
    url = ""
    if pc_name.lower() == "local":
        directory = None
        if folder == "root":
            
            directory = walk_folder(str(os.path.dirname("C:") + os.sep))
            updated_tree = []
            dir_ = ""
        else:
            f = base64.b64decode(folder)
            
            url = f.decode()
            try:
                directory = walk_folder(url)
            except FileNotFoundError as e:
                b = str.encode("C:\\")
                url_path = base64.b64encode(b)
                flash("The searched directory path was not found")
                return redirect(url_for("pc_access", pc_name = pc_name, folder = url_path))

            
            
            #directory tree handler
            dir_, updated_tree = directory_tree(url)
        session['LOCAL'] = True  
        return render_template("home.html", name = user_logged_in.username, pc_name = pc_name, info = directory, current_dir = dir_, tree = updated_tree, path_seperator = os.sep)

    else: #non local pc
        pc = LocalNetwork.query.filter_by(id = int(pc_name)).first()
        ip = pc.ip_addr
        port = pc.port

        if folder == "root":
            task = "VIEW~~C:\\"
            updated_tree = []
            dir_ = ""
            
        else:
            f = base64.b64decode(folder)
            url = f.decode()
            task = "VIEW~~" + url
        
            #directory tree handler
            dir_, updated_tree = directory_tree(url)

        directory = get_remote_dir(ip, port, task)
        session['LOCAL'] = False
        return render_template("home.html", name = user_logged_in.username, pc_name = pc_name, info = directory, tree = updated_tree, current_dir = dir_, path_seperator = os.sep)

def directory_tree(url):
    directory_tree = url.split(os.sep)
    updated_tree = []
    for each in directory_tree:
        if each == "":
            continue
        b = str.encode(each)
        url_path = base64.b64encode(b)
        updated_tree.append([url_path, each])

    dir_to_modify = url.split(os.sep)
    modified_dir = ""
    for count, each in enumerate(dir_to_modify):
        if count != len(dir_to_modify) - 1:
            modified_dir = modified_dir + each + os.sep
        else:
            modified_dir = modified_dir + each

    
    b = str.encode(modified_dir)
    dir_ = base64.b64encode(b)
    return (dir_, updated_tree)

@app.route("/pc-access-tree/<pc_name>/<file_dir>/<hard_stop>", methods = ["GET"])
@login_required
def pc_access_tree(pc_name, file_dir, hard_stop):
    #file_dir decode
    f = base64.b64decode(file_dir)
    url = f.decode()
    
    #hard_stop decode
    f = base64.b64decode(hard_stop)
    stop = f.decode()

    directory_to_iter = url.split(os.sep)
    directory = ""
    for each in directory_to_iter:
        directory = directory + each + os.sep
        if each == stop:
            break

    b = str.encode(directory)
    dir_ = base64.b64encode(b)
    return redirect(url_for("pc_access", pc_name = pc_name, folder = dir_))

@app.route("/pc-access-search", methods = ["POST"])
@login_required
def pc_access_search():
    pc_name = request.values.get("pc_name")
    search = request.values.get("search")  

    b = str.encode(search)
    url_path = base64.b64encode(b)

    return redirect(url_for("pc_access", pc_name = pc_name, folder = url_path))

def get_remote_dir(ip_addr, port, task):
    HOST = str(ip_addr) #this is the IP we connect to
    PORT = int(port)    #this is the port we connect to  
    data = None
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(task.encode('utf-8'))
        data = s.recv(1024)

        f = b''
        while data:
            if data == b'DONE':
                f += data[:len(data) - 4]
                break
            if data[-4:] == b'DONE':
                f = data[:len(data) - 4]
                break
            f += data
            data = s.recv(1024)
        
        print(f)
        f = f.decode("utf-8")
        f = ast.literal_eval(f) #converting string to dictionary to pass to template

        return f

@app.route("/check-status/<id>", methods = ["POST","GET"])
@login_required
def check_if_ready(id):
    pc_info = LocalNetwork.query.filter_by(id = int(id)).first()
    print(pc_info.ip_addr)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((pc_info.ip_addr, pc_info.port))
            return "Online"
    except Exception as e:        
        return "Offline"

@app.route("/shutdown/<pc_name>", methods = ["GET"])
@login_required  
def shutdown_remote(pc_name):
    pc_info = LocalNetwork.query.filter_by(id = int(pc_name)).first()
    HOST = pc_info.ip_addr
    PORT = pc_info.port
    data = "exit"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(data.encode('utf-8'))
            return redirect(url_for('dashboard'))
    except ConnectionRefusedError as e:
        return redirect(url_for('dashboard'))

@app.route("/home", methods=["POST", "GET"])
@login_required
def home():
    '''
    if current_user.is_authenticated is False:
        return redirect(url_for("index"))
    '''

    #directory_info = walk_root_folder("C:\\LAN_Public")

    #walk_folder("C:\LAN_Public")

    #user = User.query.filter_by(id=current_user.id).first()
    return render_template("home.html", name = "debug mode, put user.username after", info = directory_info)

@app.route("/download_file/<pc_name>/<file_dir>/<file_info>", methods=["GET"])
@login_required
def download_file(pc_name, file_dir, file_info):
    #check to make sure temp is clean, otherwise delete all exisiting files.
    path = os.path.join(app.root_path, "static" + os.sep + "temp")
    
    try:
        os.chdir(path)
    except FileNotFoundError:
        os.mkdir(path)
        os.chdir(path)

    filenames = os.listdir()
    for file in filenames:
        os.remove(path + os.sep + file)

    f = base64.b64decode(file_dir)
    file_dir = f.decode()
    
    if (pc_name != "local"):
        pc = LocalNetwork.query.filter_by(id = int(pc_name)).first()
        ip = pc.ip_addr
        port = pc.port
        file_dir = download_remote_file(ip, port, file_dir, file_info)

    return send_file(file_dir, as_attachment = True)

@app.route("/view_file/<pc_name>/<file_dir>/<file_info>", methods=["GET"])
@login_required
def view_file(pc_name, file_dir, file_info):
    #check to make sure temp is clean, otherwise delete all exisiting files.
    path = os.path.join(app.root_path, "static" + os.sep + "temp")
    os.chdir(path)
    filenames = os.listdir()
    for file in filenames:
        os.remove(path + os.sep + file)

    #decoding the file directory
    f = base64.b64decode(file_dir)
    url = f.decode()

    #file info parameter unpacking
    _, file_type, extension, file_name = make_tuple(file_info)

    #handling remote file viewing, make sure to check first that file_info has it as a viewable file type to not waste time downloading if not even viewable
    if (pc_name != "local"):
        if _ is True:
            pc = LocalNetwork.query.filter_by(id = int(pc_name)).first()
            ip = pc.ip_addr
            port = pc.port
            download_remote_file(ip, port, url, file_info)
        else:
            return request.referrer
        
    else:
        #copy folder into temp folder since cant server static images from C:\ only from static folder
        new_dir = copy(url, app.root_path + "/static/temp")
        #check to make sure is viewable type
        if _ is False:
            return redirect(url_for('home'))

    return render_template("view.html", file_dir = "temp/" + file_name, file_type = file_type, extension = extension)

def download_remote_file(ip, port, file_dir, file_info):
    HOST = ip #this is the IP we connect to
    PORT = port    #this is the port we connect to 
    _, file_type, extension, file_name = make_tuple(file_info)
    data = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = "GET$*$" + str(file_dir)
        s.sendall(message.encode('utf-8'))

        path = app.root_path + "/static" + os.sep + "temp" + os.sep + file_name
        f = open(path, "wb")
        
        data = s.recv(1024)
        while data:
            if data == b'DONE':
                break
            if data[-4:] == b'DONE':
                data_to_write = data[:len(data) - 4]
                f.write(data_to_write)
                break
            print(data)
            f.write(data)
            data = s.recv(1024)
        f.close()    
    return path

@app.route("/child-node-setup", methods = ["GET", "POST"])
@login_required
def child_node_setup():
    #shutdown server
    shutdown = request.form.get("shutdown")
    if shutdown is not None:
        return redirect(url_for('shutdown_remote', pc_name = shutdown))
    
    #delete server from db
    delete = request.form.get("delete")
    print(delete)
    all_pcs_on_network = LocalNetwork.query.all()

    if request.method == "POST" and delete is not None:
        LocalNetwork.query.filter_by(id=int(delete)).delete()
        db.session.commit()
        return redirect(url_for("child_node_setup"))

    #add server to db
    if request.method == "POST":
        pc_name = request.form.get("pc_name")
        ip_addr = request.form.get("ip")
        port = request.form.get("port")
        new_pc = LocalNetwork(pc_name = pc_name, ip_addr = ip_addr, port = port, date_added = datetime.utcnow())
        db.session.add(new_pc)
        db.session.commit()
        return redirect(url_for("child_node_setup"))
    

    return render_template("child-node.html", name = user_logged_in.username, pcs = all_pcs_on_network)

@app.route("/download-server", methods = ["GET"])
@login_required
def download_server():
    download_link = os.getcwd() + os.sep + "app" + os.sep + "server.py" #make sure sending .exe
    return send_file(download_link, as_attachment = True)

