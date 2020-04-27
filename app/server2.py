#!/usr/bin/env python3


#output ip and socket
#check to make sure correct operating system
#check if folder exists in C drive
#connect this endpoint to the head
#the head adds this server to its database as a list to try

import socket

hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    
print("Your Computer Name is:" + hostname)    
print("Your Computer IP Address is:" + IPAddr)    


HOST = IPAddr  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)



#this is an endpoint
#user startsup endpoint, adds the ip address in the web app
#the web app then searches for all endpoints that are online (try and catch)
#then when a user wants files from an endpoint, it maintains a connection with that endpoint until moving on to the next
#endpoint should be an exe that runs in the background on a windows pc