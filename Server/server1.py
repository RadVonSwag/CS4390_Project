import socket;
import sys;
import os;
import pickle;

S_HOST = "127.0.0.1"  # The server's hostname or IP address
S_PORT = 65432  # The port used by the server

R_HOST = "127.0.0.2"
R_PORT = 65431

Direc = os.path.normpath("files")
files = os.listdir(Direc)
#files = [f for f in files if os.path.isfile(Direc+'/'+f)]
#print(files)
 
# result = []
# def filePath(file, path):
#     for root, dirs, files in os.walk(Direc):
#         if file in files:
#             result.append(os.path.join(root, file))
#     return result

# f1 = open()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created!")

#Bind socket to localhost under defined port
serverSocket.bind((S_HOST, S_PORT))
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
            msg = pickle.dumps(files)
            conn.send(msg)
            
            file = (conn.recv(1024)).decode()
            print("Message: " + file)
            # path = filePath(file, Direc)
            # media = open(path, "r")
            # msg = media.read()
            try:
                fileIndex = files.index(file)
                if files[fileIndex] == file:
                    f =  os.path.normpath(file)
            except ValueError:
                print("The files does not exist.")
                
            conn.send(msg)
        else:
            # Close connectionSocket            
            conn.close()
            print("Connection closed!")      
    except IOError as err:
        # Send response message for invalid file
        print("IOError: " + str(err))
        conn.close()
    