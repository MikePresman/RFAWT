# RFAWT
Remote File Access Web Tool
![](https://i.imgur.com/s0ayhd4.png)
<br/>
![](https://i.imgur.com/11Fybxd.png)

#Reproducing a Working State
1. Setup Environment on Command Prompt. V2.0 Now supporting WSL
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

#V2.0
1. Supporting WSL
