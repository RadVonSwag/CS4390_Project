import socket;
import sys;
import os;

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

Direc = os.path.normpath("files")
files = os.listdir(Direc)
files = [f for f in files if os.path.isfile(Direc+'/'+f)]
#the next several lines turn files into a single string with newline characters separating the file names
filesConcatenated = files[0]
index = 0
for file in files:
    if index != 0:
        filesConcatenated = filesConcatenated + '\n' + file

#this creates a bytearray that can be sent through the socket
filesEncoded = filesConcatenated.encode()

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

        if message == 'GET':
            print("Message: " + message)
            conn.send(filesEncoded)
        elif message[0:2] == 'GET': #message is from renderer, convert from newline-separated string to list of strings
            fileList = []
            fileName = ""
            message = message[3:]
            for char in message:
                if char == '\n':
                    fileList.append(fileName)
                    fileName = ""
                else:
                    fileName = fileName + char
            fileList.append(fileName)
            #send each file listed to renderer
            for file in fileList:
                try:
                    with open(file, "rb") as f:
                        sendStr = "SEND"
                        sendStrEncoded = sendStr.encode()
                        conn.sendall(sendStrEncoded)
                        while True:
                            rendererPacket = f.read(1024)
                            if not rendererPacket:
                                break
                            conn.sendall(rendererPacket)
                        eofStr = "EOF"
                        eofStrEncoded = eofStr.encode()
                        conn.sendall(eofStrEncoded)
                except:
                    print("Incorrect Filename...")
                    
        else:
            print("Invalid input")
    except IOError as err:
        # Send response message for invalid file
        print("IOError: " + str(err))

conn.close()