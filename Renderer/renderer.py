import socket
import sys
import util
from util import *

#Start listen SERVER
def start_renderer():
    render_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Render Socket created!")
    
    try:
        #Bind socket to localhost and port
        render_socket.bind(('', Port.RENDER))
        print("Render Socket bind complete")

    except socket.error as msg:
        print("Bind failed. Error: " + str(msg))
        sys.exit()

    # if SERVER is busy serving the client; you can have up to 5 client waiting to be serve
    render_socket.listen(5)
    print("Socket now listening")

    positive= True
    while positive:
        # Establish connections
        # Accept all incoming connections
        connection_socket, addr = render_socket.accept()
        print("Incoming Source address: " + str(addr))
        
        try:
            # Receive message from the socket
            message = connection_socket.recv(1024)
            print("Message: " + str(message))
            
            # Decode the message
            message = util.json_loads_byteified(message)
            type = message.get("type")
            
            if type == Message.REQUEST:
                # Convert request back to JSON and send to Server
                data = json.dumps(message)
                
                #Create TCP socket
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                send_request(client_socket, data)
                
                # Decode the received file
                data = client_socket.recv(2048)
                client_socket.close()
                
                payload = util.json_loads_byteified(data)
                if payload["type"] == Message.ERROR:
                    print(payload["content"])
                else:            
                    file_name = payload["fileName"]
                    file_data = payload["content"]
                    
                    print("Displaying file: " + file_name)
                    print(file_data)
                
            elif type == Message.EXIT:
                positive = False
                data = json.dumps({"content": "[RENDER] shutting down"})
                connection_socket.sendall(data)

            
            # Close connection_socket
            connection_socket.close()
            print("Connection closed!")
                
        except IOError as err:
            # Send SEND message for invalid file
            print("IOError: " + str(err))
            connection_socket.close()
            
    render_socket.shutdown(socket.SHUT_RDWR)
    render_socket.close()
    print("Exiting...")
    
    
# function to call when sending back requested files
def send_request(client_socket, payload):
    client_socket.connect((Address.SERVER, Port.SERVER))
    client_socket.sendall(payload)
    
    
start_renderer()
    