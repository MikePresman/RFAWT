#!/usr/bin/env python3
#this files requires file_manager.py
import socket
import os
from file_manager import walk_root_folder, walk_folder
import json
import sys
import zlib
import requests
import io
import struct

def server():
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

            
                #get file here and send it over
                if file_path is not None:
                    file_to_send = open(file_path, "rb+")
                    data_to_send = file_to_send.read(1024)
                    while (data_to_send):
                        print(data_to_send)
                        print("---------------------")
                        conn.send(data_to_send)
                        data_to_send = file_to_send.read(1024)
                    file_to_send.close()
                    print("Finished")
                    conn.sendall(b"DONE")
                    
                if data:
                    action = None
                    try:
                        payload = data.decode("utf-8").split("~~")
                        action = payload[0]
                        URI = payload[1]
                    except Exception as e:
                        pass

                    
                    if data.decode('utf-8') == "exit":
                        sys.exit()


                    #get_remote_dir    
                    if action is not None and action == "VIEW":
                        #break this up into a loop
                        new_data = str(walk_folder(URI)).encode("utf-8")
                        starting_point = 0
                        ending_point = 1024
                        data_to_send = new_data[starting_point:ending_point]

                        flag = False
                        while (data_to_send):
                            conn.send(data_to_send) #block send of 1024 bytes

                            #new block allocation, shifting down 1024 bytes
                            temp = ending_point
                            starting_point = ending_point
                            ending_point = temp + 1024
                            
                            #need to check whether the newly allocated block isnt out of range (i.e. too small)
                            #if the newly allocated block size isnt too small, we send it
                            if (len(new_data[starting_point:ending_point]) >= 1024):
                                data_to_send = new_data[starting_point:ending_point]
                            #last block in the sequence that doesnt full fit 1024
                            else:
                                final_byte = 1024
                                while(final_byte >= len(new_data[starting_point:ending_point])):
                                    final_byte = final_byte - 1
                                    if final_byte == 0:
                                        break
                                
                                ending_point = final_byte + starting_point
                                conn.send(new_data[starting_point:ending_point+1])
                                conn.sendall(b"DONE")
                                flag = True
                                break
                conn, addr = s.accept() #accept next connection
                
                
                
                
                

if __name__ == "__main__":
    server()

                    




            
#this is an endpoint
#user startsup endpoint, adds the ip address in the web app
#the web app then searches for all endpoints that are online (try and catch)
#then when a user wants files from an endpoint, it maintains a connection with that endpoint until moving on to the next
#endpoint should be an exe that runs in the background on a windows pc