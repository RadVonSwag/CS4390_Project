'''
Server class
Listens for requests made by the Controller and Renderer
Sends a list of files to Controller
Sends actual files to Renderer
https://github.com/bippity/NetworkApplicationProject/
'''

import json
import os
from os import listdir
from os.path import isfile, join
import socket
import sys
import util
from util import *

data_folder = os.path.normpath("files")


#Start listen SERVER
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #So you won't have to wait for address to timeout
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created!")
    
    try:
        #Bind socket to localhost under defined port
        server_socket.bind(('', Port.SERVER))
        print("Socket bind complete")
    except socket.error as message:
        print("Bind failed. Error: " + str(message))
        sys.exit()
    
    #Start listening on socket
    # 2 connections kept waiting if SERVER busy. 3rd socket will be refused
    server_socket.listen(2)
    print("Socket now listening")

    positive = True
    while positive:
        # Establish connections
        # Accept all incoming connections
        connection_socket, addr = server_socket.accept()
        print("Incoming Source address: " + str(addr))
        
        try:
            # Receive message from the socket
            #1024 = max size in bits to be received at once
            message = connection_socket.recv(1024)
            print("Message: " + str(message))
            
            # Decode the message
            message = util.json_loads_byteified(message)
            type = message.get("type")
            
            if type == Message.GET:
                files = list_files()
                #Convert list to JSON to send across socket
                data = json.dumps({"content": files})
                connection_socket.sendall(data)
                
            elif type == Message.REQUEST:
                # Obtain file
                file_name = message.get("content")
                send_file(connection_socket, file_name)
                
            elif type == Message.EXIT:
                positive = False
                data = json.dumps({"content": "[SERVER] shutting down"})
                connection_socket.sendall(data)

            
            # Close connection_socket
            connection_socket.close()
            print("Connection closed!")
                
        except IOError as err:
            # Send SEND message for invalid file
            print("IOError: " + str(err))
            info_payload = {}
            info_payload["type"] = Message.ERROR
            info_payload["content"] = "File does not exist: " + file_name
            connection_socket.sendall(json.dumps(info_payload))
            connection_socket.close()
            
    server_socket.shutdown(socket.SHUT_RDWR)
    server_socket.close()
    print("Exiting...")

# Encode the data and send it
def send_file(connSocket, fileName):
    #Open file in read-binary
    file = open(join(data_folder, fileName), "rb")
    info_payload= {}
    info_payload["type"] = Message.SEND
    info_payload["fileName"] = fileName
    info_payload["content"] = file.read()
    data = json.dumps(info_payload)
    connSocket.sendall(data)

# Returns a list of files inside the "files" directory
def list_files():
    files = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]
    files.sort()
    return files



start_server()
