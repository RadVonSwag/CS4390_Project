import socket
import util
import sys
from util import *
#establish TCP connection with server
serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, TCP
serverSocket.connect((Address.SERVER, Port.SERVER))
filemap = {}

def getFileList():
    serverSocket.sendall('getfilelist')
    try:
        serverSocket.listen(10)
        fileList = open(serverSocket.recv(1024, 'r'))
        lines = fileList.readlines()
        return lines

    except socket.error:
            print('received nothing')
#send request to the server for a list of files stored

def displayFileList(lines):
    i = 0
    print("Choose which file you would like to stream by typing its name\nHit Enter once you've typed the name of the file you would like to stream.\n Input \"quit\" if you wish to quit the application.")
    for line in lines:
        i += 1
        print("{} {}".format(i, line.strip()))
        filemap[i] = line.strip()

def createRenderList(userinput, filemap):
    userinputmap = {}

    #put the user's choices into a new dict
    for key in userinput:
        userinputmap[int(key)] = filemap[int(key)]

    #create file with user's choices to send to renderer
    renderlistfile = open('Controller/renderlistfile.txt', 'w')
    for key, value in userinputmap.items():
        renderlistfile.write('%s %s\n' % (key, value))
    filename = renderlistfile.name
    renderlistfile.close()
    return filename

def sendToRenderer(filename):
    #establish TCP connection with Renderer
    rendererSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        rendererSocket.connect((Address.RENDER, Port.RENDER))
    except socket.error as msg:
        print("Failed to connect to Renderer. Error:" + str(msg))
        sys.exit()

    file = open(filename, 'r')
    #send user selections file to renderer
    rendererSocket.sendall(file)


choice = 'continue'
while choice != 'quit':
    print('CS-4390 Network File Streaming Application\n===========================================')
    displayFileList()
    choice = input('File: ')
    renderfile = createRenderList(choice, filemap)
    sendToRenderer(renderfile)


