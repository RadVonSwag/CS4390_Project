import socket
#establish TCP connection with server
serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, TCP
serverSocket.connect(('127.0.0.1', 126)) #server just running on local host using random port (126)

#send request to the server for a list of files stored
serverSocket.sendall('getfilelist')

#wait for response from server (expecting a file in return)
try:
    serverSocket.listen(10)
    fileList = open(serverSocket.recv(1024, 'r'))
    lines = fileList.readlines()
    filemap = {}

    #print the available files returned from the server to the console and store the options in a dict
    i = 0
    print("Choose which files you would like to stream by typing their numbers.\nHit Enter once you've selected the files you would like to stream.")
    for line in lines:
        i += 1
        print("{} {}".format(i, line.strip()))
        filemap[i] = line.strip()

except socket.error:
        print('received nothing')

#accept user input
userinput = input('I would like to stream files: ')
userinputmap = {}

#put the user's choices into a new dict
for key in userinput:
    userinputmap[int(key)] = filemap[int(key)]

#create file with user's choices to send to renderer
renderlistfile = open('Controller/renderlistfile.txt', 'w')
for key, value in userinputmap.items():
    renderlistfile.write('%s %s\n' % (key, value))


#establish TCP connection with Renderer
rendererSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rendererSocket.connect(('127.0.0.1', 252))

#send user selections file to renderer
rendererSocket.sendall(renderlistfile)
renderlistfile.close()



