#this script is for testing (will delete later)

import os
print(os.getcwd())
fileList = open('Controller/temp.txt', 'r')
lines = fileList.readlines()
i = 0
filemap = {}
for line in lines:
    i += 1
    print("{} {}".format(i, line.strip()))
    filemap[i] = line.strip()
print(filemap)

userinput = input('I would like to stream files: ')
userinputmap = {}

for key in userinput:
    userinputmap[int(key)] = filemap[int(key)]
    print(filemap[int(key)])

renderlistfile = open('Controller/renderlistfile.txt', 'w')
for key, value in userinputmap.items():
    renderlistfile.write('%s %s\n' % (key, value))
renderlistfile.close()