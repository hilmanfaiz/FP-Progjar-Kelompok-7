import socket
import sys

host = 'localhost'
port = 5006
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
sys.stdout.write('>>')
contentlength = 0
tab = "\t"

while 1:
    line = sys.stdin.readline()
    if line == '\n':
        break
    s.send(line)
    data = s.recv(size)
    print data
    requestheader = line.split(" ")[0]
    if requestheader.lower() == "get" and 'Content-Length' in data:
        contentlength = int(data.split("Content-Length: ")[1].split("\r\n")[0])
        datafile =s.recv(contentlength)
        print datafile
    sys.stdout.write('>>')
s.close()
 
    
