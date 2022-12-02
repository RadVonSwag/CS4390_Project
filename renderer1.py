import socket;
import os;

R_HOST = "127.0.0.2"
R_PORT = 65431

S_HOST = "127.0.0.1"
S_PORT = 65432

renderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Render Socket created!")

renderSocket.bind((R_HOST, R_PORT))
print("Render Socket bind complete")

renderSocket.listen(2)
print("Socket now listening")

forwardFlag = False
forwardFrom = ""
forwardToIP = ""
forwardToPort = ""
sendFlag = False
sendFrom = ""
handled = False

while(2):
    conn, addr = renderSocket.accept()
    print("Incoming Source address: " + str(addr))
    
    try:
        handled = False
        message = (conn.recv(1024))
        if forwardFlag:
            if forwardFrom == str(addr):
                forwardSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                forwardSocket.connect(forwardToIP,int(forwardToPort))
                forwardSocket.sendall(message)
                forwardSocket.close()
                handled = True
                forwardFlag = False
                
        if sendFlag:
            if sendFrom == str(addr):
                if message.decode() == "EOF":
                    sendFlag = False
                else:
                    with open("outputFile.txt","wb") as out:
                        out.write(message)
                    with open("outputFile.txt","r") as out:
                        print(out.read())
                handled = True
        if not handled:
            input = message.decode()
            if input[0:6] == "FORWARD":
                spaces = 0
                for char in input:
                    if char = ' ':
                        spaces += 1
                    elif spaces == 1:
                        forwardToIP = forwardToIP + char
                    elif spaces == 2:
                        forwardToPort = forwardToPort + char
                forwardFlag = True
                forwardFrom = addr
            elif input[0:3] == "SEND":
                sendFlag = True
                sendFrom = str(addr)
        conn.close()
    except IOError:
        conn.close()