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

@app.route("/", methods=["POST", "GET"])
def index():
    return redirect(url_for("home"))
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
def dashboard():
    pcs_on_network = LocalNetwork.query.all()

    #change this
    '''
    pcs_online = []
    #try connection to see which ones are open, then remove the ones that arent
    for each in pcs_on_network:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((each.ip_addr, each.port))
                pcs_online.append([True, each])
        except Exception as e:
            pcs_online.append([False, each]) #not online
    print(pcs_online)
    '''

    #implement check if online
    return render_template("dashboard.html", pcs = pcs_on_network)

@app.route("/pc-access/<pc_name>", methods = ["GET"])
def pc_access(pc_name):
    if pc_name.lower() == "local":
        directory = walk_folder("C:/")
        return render_template("home.html", name = "debug mode, put user.username after", info = directory)
    #MAKE IT JUST LIKE FILE EXPLORER, DONT HAVE TO HAVE DROP DOWN BOX BUT JUST KEEP CLICKING ON NEXT FOLDER
    #THE PARAMETER WILL SEARCH FOR ALL ROOT DIRECTORIES
    #BUT FIRST NEED TO ESTABLISH SOCKET CONNECTION IF PC_NAME IS NOT LOCAL


    return "Hello World"



#have to figure out how to do walk_root_folder but handle for all available folders on the PC

@app.route("/getReady/<id>", methods = ["POST","GET"])
def check_if_ready(id):
    pc_info = LocalNetwork.query.filter_by(id = int(id)).first()
    print(id + "  Here")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((pc_info.ip_addr, pc_info.port))
            return "Online"
    except Exception as e:
        return "Offline"


@app.route("/home", methods=["POST", "GET"])
def home():
    '''
    if current_user.is_authenticated is False:
        return redirect(url_for("index"))
    '''
    

    directory_info = walk_root_folder("C:\\LAN_Public")

    walk_folder("C:\LAN_Public")



    #user = User.query.filter_by(id=current_user.id).first()
    return render_template("home.html", name = "debug mode, put user.username after", info = directory_info)



@app.route("/download_file/<file_dir>", methods=["GET"])
def download_file(file_dir):
    return send_file(file_dir, as_attachment = True)


@app.route("/view_file/<file_name>/", methods=["GET", "POST"])
def view_file(file_name):
    if request.method == "POST":
        #check to make sure temp is clean, otherwise delete all exisiting files.
        directory = os.getcwd() + r'\app\static\temp'
        for root, dirs, files in os.walk(directory):
            for file in files:
                f = open(str(directory) + "\\" + str(file), 'w')
                if f.closed is False:
                    f.close()
                os.remove(directory + "\\" + file)

        data = request.values.get("view").split(":")

    #copy folder into temp folder since cant server static images from C:\ only from static folder
    new_dir = copy(data[0] + ":" + data[1], app.root_path + "/static/temp")
    _, file_type, extension, file_name = make_tuple(data[2])

    #check to make sure is viewable type
    if _ is False:
        return redirect(url_for('home'))
    
    return render_template("view.html", file_dir = "temp/" + file_name, file_type = file_type, extension = extension)


@app.route("/getfile", methods = ["POST", "GET"])
def get_file():
    r = request.get_data() #getting binary data that we sent
    raw = (r.decode("utf-8"))
    return raw

@app.route("/remote_view_file/<file_name>/", methods = ["POST","GET"])
def remote_view_file(file_name):
    info = request.form.get("view")

    HOST = '192.168.0.11' #this is the IP we connect to
    PORT = 65432    #this is the port we connect to   
    data = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        #sending data to server to get the file we want
        message = "GET$*$" + str(info)
        s.sendall(message.encode('utf-8'))
        


        #only getting a quarter of the image        
        #recieving the file back
        
    
        
        #read how send_file in flask is implemented
        path = "B:/Downloads/file.pdf"
        #THIS WORKS
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
    
        
        '''V1 WORKING CORRESPONDING
         f = open("/Users/mike/Downloads/picture.jpg", "wb")
        
        data = s.recv(1024)
        while data:
            print(data)
            f.write(data)
            data = s.recv(1024)
        f.close()
        '''
        
        
    
    return redirect(url_for("home"))




#make this is a paramterized URL with the computer name
@app.route("/get/<message>", methods = ["GET"])
def get_dir_info(message):
    HOST = '192.168.0.11' #this is the IP we connect to
    PORT = 65432    #this is the port we connect to   
    data = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode('utf-8'))
        
        #buffer bug, try compressing it first
        data = s.recv(5012)
        #flask --run host = 0.0.0.0
        f = data.decode("utf-8") # WE GET STRING HERE, NEED TO CONVERT TO DICTIONARY FOR THE TEMPLATE
    
        f = ast.literal_eval(f) #converting string to dictionary to pass to template
        

        #after buffer bug is fixed work on remote_view_file to get files across to remote client
        

        #data = json.loads(data.decode("utf-8"))
    
    return render_template("home.html", name = "debug mode, put user.username after", info = f)

@app.route("/child-node-setup", methods = ["GET", "POST"])
def child_node_setup():
    delete = request.form.get("delete")
    print(delete)
    all_pcs_on_network = LocalNetwork.query.all()

    if request.method == "POST" and delete is not None:
        LocalNetwork.query.filter_by(id=int(delete)).delete()
        db.session.commit()
        return redirect(url_for("child_node_setup"))


    if request.method == "POST":
        pc_name = request.form.get("pc_name")
        ip_addr = request.form.get("ip")
        port = request.form.get("port")
        new_pc = LocalNetwork(pc_name = pc_name, ip_addr = ip_addr, port = port, date_added = datetime.utcnow())
        db.session.add(new_pc)
        db.session.commit()
        return redirect(url_for("child_node_setup"))
    

    return render_template("child-node.html", pcs = all_pcs_on_network)

@app.route("/tryconnection", methods = ["GET"])
def listen():
    HOST = '192.168.0.14' #this is the IP we connect to
    HOST1 = '192.168.0.14' #this is the IP we connect to
    PORT = 65431    #this is the port we connect to   
    PORT2 = 65432    #this is the port we connect to   

    info = [[HOST, PORT], [HOST1, PORT2]]
    for each in info:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((each[0], each[1]))
                s.sendall(b'Hello World')
                data = s.recv(1024)
        except ConnectionRefusedError as e:
            print(e)
            return redirect(url_for("home"))
        print("Recieved", repr(data))
        continue
    return redirect(url_for("home"))

@app.route("/download-server", methods = ["GET"])
def download_server():
    download_link = os.getcwd() + "\\app\\server.py" #make sure sending .exe
    return send_file(download_link, as_attachment = True)

