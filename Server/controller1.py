import socket;
import pickle;

HOST = "127.0.0.1"
PORT = 65432

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
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
        clientSocket.connect((HOST, PORT))
        data = "files"
        clientSocket.send(data.encode())

        data = clientSocket.recv(1024)
        files = pickle.loads(data)

        print("List of media files:")
        for f in files:
            print(f)
        
        fileName = input("Enter the file name: ")
        clientSocket.send(fileName.encode())
        

    

    
    