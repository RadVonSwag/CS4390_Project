import socket;
import sys;
import os;
import pickle;

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

Direc = os.path.normpath("files")
files = os.listdir(Direc)
files = [f for f in files if os.path.isfile(Direc+'/'+f)]
msg = pickle.dumps(files)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created!")

#Bind socket to localhost under defined port
serverSocket.bind((HOST, PORT))
print("Socket bind complete")

#Start listening on socket
serverSocket.listen(2)
print("Socket now listening")

while(2):
    # Establish connections
    # Accept all incoming connections
    conn, addr = serverSocket.accept()
    print("Incoming Source address: " + str(addr))

    try:
        # Receive message from the socket
        message = (conn.recv(1024)).decode()

        if message == 'files':
            print("Message: " + message)
            conn.send(msg)
        elif message == 'hello.txt':
            print("Message: " + message)
            conn.send()
        else:
            # Close connectionSocket            
            conn.close()
            print("Connection closed!")      
    except IOError as err:
        # Send response message for invalid file
        print("IOError: " + str(err))
        conn.close()
    