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

while(2):
    conn, addr = renderSocket.accept()
    print("Incoming Source address: " + str(addr))
    
    try:
        message = (conn.recv(1024)).decode()
        print("Message: " + str(message))
        
        path = os.path.dirname(__file__) + "\\files\\" + str(message)
        
        file = open(path, "r")
        data = file.read()
        
        print("\n" + data + "\n")
        
        #conn.send(data.encode("utf-8"))
        
    except IOError:
        conn.close()