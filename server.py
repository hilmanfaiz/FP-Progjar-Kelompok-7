#!/usr/bin/env python
#http://ilab.cs.byu.edu/python/threadingmodule.html 
import select
import socket
import sys
import threading

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(5)
        
    def run(self):
        self.open_socket()
        input = [self.server, sys.stdin]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)
                    print "new client connected: ", c,

                elif s == sys.stdin:
                    print "junk"                    
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()
        print "Server closed"

class Client(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.path = os.path.dirname(os.path.abspath(__file__))+'/halamanWeb/'
        self.pathdefault = os.path.dirname(os.path.abspath(__file__))+'/halamanWeb/' #jangan diubah2 di bawah yaa
        self.requestHeader = ""
        self.filesize = 0
        self.header = ""
        self.data = ""
 
    def run(self):
        running = 1
        while running:
            try:
                data = self.client.recv(self.size)
            except:
                self.client.close()
                running = 0                
            print 'recv: ', self.address, data #debugging
            
            
            if data:
                self.requestHeader = ""
                self.requestHeader = data.split(" ")[0]
                str1 = self.requestHeader
                self.requestHeader = str1.lower()
                reqfile = data.split("/")[1].split("\n")[0]
                if (self.requestHeader == "get" or self.requestHeader == "head" ):
                    self.path = self.pathdefault + reqfile
                    self.do_GET_HEAD()
                elif(self.requestHeader == "post"):
                    self.path = self.pathdefault + reqfile
                    self.do_POST()
           else:
                self.client.close()
                running = 0

if __name__ == "__main__":
    s = Server()
    s.run() 
