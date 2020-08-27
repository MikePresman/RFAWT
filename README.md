# RFAWT
Remote File Access Web Tool
![](https://i.imgur.com/s0ayhd4.png)
<br/>
![](https://i.imgur.com/11Fybxd.png)

#Reproducing a Working State
1. Setup Environment on Command Prompt ~~(WSL, for all its beauty doesnt accept Python's escape characters in the same manner)~~ Now supporting WSL !!!
2. Install Requirements
3. set FLASK_APP=run.py
4. Make sure you setup your desired REGISTER_KEY in the config.py
5. Register or use default account (Username: Admin, Password: 1234)
6. Login into your Routers network
7. Add port forwarding for the PC where this server is being run
....(Port 5000, the IP Address will be the local ip address of the PC you are running the server on)
.... Just do ipconfig to get your local ip or in another console run, python app/server.py, itll give you the IP
8. Now to the flask server publicy, simply do flask run --host=0.0.0.0
9. To connect, find your network IP, and connect through the browser with <ip_address>:<port> (The default port is 5000)


#Requirements
alembic==1.4.2
blinker==1.4
certifi==2020.4.5.1
chardet==3.0.4
click==7.1.2
Flask==1.1.2
Flask-Login==0.5.0
Flask-Mail==0.9.1
Flask-Migrate==2.5.3
Flask-SQLAlchemy==2.4.3
Flask-WTF==0.14.3
idna==2.9
itsdangerous==1.1.0
Jinja2==2.11.2
Mako==1.1.3
MarkupSafe==1.1.1
python-dateutil==2.8.1
python-editor==1.0.4
requests==2.23.0
six==1.15.0
SQLAlchemy==1.3.17
urllib3==1.25.9
Werkzeug==1.0.1
WTForms==2.3.1
