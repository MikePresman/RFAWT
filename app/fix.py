import socket
HOST = '192.168.0.14' #this is the IP we connect to
PORT = 65432    #this is the port we connect to   

    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello World')
    data = s.recv(1024)

print("Recieved", repr(data))
