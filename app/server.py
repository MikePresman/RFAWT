#!/usr/bin/env python3


#output ip and socket
#check to make sure correct operating system
#check if folder exists in C drive
#connect this endpoint to the head
#the head adds this server to its database as a list to try


#then work on remotely seeing all files on client pc (through server) and fetching them for download


import socket
import os
from file_manager import walk_root_folder
import json
import sys
import zlib
import requests


def send_folder_data(conn):
    data = walk_root_folder()
    s = json.dumps(data).encode('utf-8')
    conn.send(s)


#NEED TO RESTART SERVER EVERYTIME MAKING CHANGES


#check if folder lan-explorer exists, if it doesnt make it under C:\
'''
root_dir = "C:\\LAN_Public"
if os.path.exists(root_dir) is False:
    os.mkdir(root_dir)
else:
    print("Local Network Directory Exists")
os.chdir(root_dir)
'''


#start server connection
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)   
HOST = IPAddr       # Standard loopback interface address (localhost)
PORT = 65432        

print("Your Computer Name is:" + hostname)    
print("Your Computer IP Address is:" + IPAddr)    
print("Your Computer Port is:" + str(PORT))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(1024) #receiving data persistently
            non_raw_data = data.decode("utf-8")
            print(non_raw_data)
            
            #check to see whether we want to get a file
            file_path = None
            try:
                if non_raw_data.split("$*$")[0] == "GET":
                    split_data = non_raw_data.split("$*$")
                    file_path = split_data[1]
            except Exception as e:
                pass


            print(file_path)
            #get file here and send it over
            if file_path is not None:
               file_to_send = open(file_path, "rb+")
               data_to_send = file_to_send.read(1024)
               while (data_to_send):
                   print(data_to_send)
                   print("-----------------------------")
                   conn.send(data_to_send)
                   data = data_to_send.read(1024)
                file_to_send.close()
                print("finished")
            


        
            new_data = str(walk_root_folder("C:\\Users\\Mike\\Downloads")).encode("utf-8")
        
            if data:
                if data.decode('utf-8') == "exit":
                    sys.exit()
                conn.sendall(new_data)
            conn, addr = s.accept() #accept next connection
            
            
            
            
            

        

                    




            
#this is an endpoint
#user startsup endpoint, adds the ip address in the web app
#the web app then searches for all endpoints that are online (try and catch)
#then when a user wants files from an endpoint, it maintains a connection with that endpoint until moving on to the next
#endpoint should be an exe that runs in the background on a windows pc