import socket;
import pickle;

S_HOST = "127.0.0.1"
S_PORT = 65432

R_HOST = "127.0.0.2"
R_PORT = 65431
    
def menu():
    print("Network Application:\n" + "1) Files in Server.\n" + "2) Open File.\n" + "3) Exit.\n")

    while True:
        try:
            inputVal = int(input("Choose an option: "))
        except ValueError:
            print("Invalid option. Please try again.")
            continue
        
        if inputVal < 1 or inputVal > 3:
            print("Invalid option. Out of range (1-3).")
        else:
            break
    
    return inputVal

val = int
while val != 3:
    val = menu()
    
    if val == 1:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((S_HOST, S_PORT))
        data = "files"
        clientSocket.send(data.encode())

        data = clientSocket.recv(1024)
        files = pickle.loads(data)

        print("\nList of media files:")
        for f in files:
            print(f)
        
        print("\n")
        
        clientSocket.close()
        # fileName = input("Enter the file name: ")
        # clientSocket.send(fileName.encode())
        
        # data = clientSocket.recv(1024)
        # choosenFile = pickle.loads(data)
        
        #print(choosenFile)
    elif val == 2:
        client2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2Socket.connect((R_HOST, R_PORT))
        
        #send the file name to renderer
        file = str(input("\nEnter file name: "))
        client2Socket.send(file.encode())
        
        #get the data of the file requested from renderer
        data = client2Socket.recv(1024).decode("utf-8")
        print("\n" + data +"\n")
        
        client2Socket.close()
        
        
        

    

    
    