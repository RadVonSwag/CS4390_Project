'''
Controller class
Displays the menu to the user
Can request list of files in Server
Tells the Renderer to request a file from the Server
'''

import json
import socket
import sys
import utils
from utils import *


def get_menu_input():
    menu = ("==Network Application==\n"
            "1) List files from the SERVER.\n"
            "2) Open file.\n"
            "3) Exit.\n")
    while True:
        try:
            print("yor option is 1 or 2 or 3")
            inputVal = int(raw_input(menu + "Choose an option: "))
        except ValueError:
            print("Invalid option. Please try again.")
            continue

        if inputVal < 1 or inputVal > 3:
            print("Invalid option. Out of range (1-3).")
        else:
            break

    return inputVal


#Lists SERVER files in a list
def get_server_files():
    #Create info_payload message
    info_payloads = json.dumps({"type": Message.FETCH})
    data = send_message(Message.FETCH, info_payloads)
    
    #Decode the recieved data from unicode, then Parse data into JSON format
    data = utils.json_loads_byteified(data)
    files = data.get("content")

    print("List of files in Server:")
    print(str(files))

def close_server_file():
    print("Closing file")
    
    
def send_message(type, info_payload):
    #Create TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Determine what message to send
    #Send fetch request of SERVER files
    if type == Message.FETCH:
        client.connect((Address.SERVER, Port.SERVER))
        client.sendall(info_payload)
        
    elif type == Message.REQUEST:
        client.connect((Address.RENDER, Port.RENDER))
        client.sendall(info_payload)
        
    elif type == Message.EXIT:
        # Close the SERVER
        client.connect((Address.SERVER, Port.SERVER))
        client.sendall(info_payload)
        client.close()
        
        # Close the RENDER
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((Address.RENDER, Port.RENDER))
        client.sendall(info_payload)
        
    data = client.recv(1024)
    #print("Raw data: " + str(data))
    client.close()
    return data

# Tells Server to shutdown/stop
def close_server():
    payload = json.dumps({"type": Message.EXIT})
    data = send_message(Message.EXIT, payload)
    data = utils.json_loads_byteified(data)
    msg = data.get("content")
    print(str(msg))





#Tell RENDER to request the specified file via ID from the Server
def open_server_file():
    file_name = raw_input("Enter file name: ")

    # Create message for Renderer
    payload = {}
    payload["type"] = Message.REQUEST
    payload["content"] = file_name
    payload = json.dumps(payload)

    # Send message and get response
    data = send_message(Message.REQUEST, payload)



# Map inputs to functions
val = int
while val != 3:
    val = get_menu_input()

    if val == 1:
        get_server_files()
    elif val == 2:
        open_server_file()
    elif val == 3:
        print("Exiting...")
        close_server()
        sys.exit()
        
    print("\n")


