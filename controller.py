import socket
#establish TCP connection with server
serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, TCP
serverSocket.connect(('127.0.0.1', 65432)) #server just running on local host using random port (126)

#send request to the server for a list of files stored
request = "GET"
requestEncoded = request.encode()
serverSocket.sendall(requestEncoded)

#wait for response from server (expecting a file in return)
try:
    serverSocket.listen(10)
    byteStream = open(serverSocket.recv(1024, 'r'))
    #turns the UTF-8 encoded bytestream into a string
    filesStr = byteStream.decode()
    #next 8 lines turn the string into a list of strings that were separated by newline characters
    files = []
    curFile = ""
    for char in filesStr:
        if char == '\n':
            files.append(curFile)
            curFile = ""
        else:
            curFile = curFile + char
    files.append(curFile)

    #print the available files returned from the server to the console and store the options in a dict
    print("Choose which files you would like to stream by typing their numbers separated by spaces.\nHit Enter once you've selected the files you would like to stream.")
    index = 0
    for file in files:
        print(index + ") " + file)
        index += 1

except socket.error:
        print('received nothing')

#accept user input
userinput = input('I would like to stream files: ')
filesChosen = "GET"
key = ""

#put the user's choices into a string with file names separated by newline characters
for char in userinput:
    if char == ' ':
        filesChosen = filesChosen + files[int(key)] + '\n'
        key = ""
    else:
        key = key + char
filesChosen = filesChosen + files[int(key)]
filesChosenEncoded = filesChosen.encode()

#establish TCP connection with Renderer
rendererSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rendererSocket.connect(('10.0.0.3', 2520))

#send user selections file to renderer
forwardStr = "FORWARD\n" + "10.0.0.1\n" + "1260"
forwardStrEncoded = forwardStr.encode()
rendererSocket.sendall(forwardStrEncoded)
rendererSocket.sendall(chosenFilesEncoded)
renderlistfile.close()



