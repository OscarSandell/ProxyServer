#!/usr/bin/env python3
from socket import *
import os
class Server:

    def __init__(self):
        print("Server Created.")

    #Takes portnumber as argument and binds the port to a TCP socket, we are using ipv4.
    def Listen(self,portnumber):
        self.portnumber = portnumber
        self.serverSocket = socket(AF_INET,SOCK_STREAM)

        #We use os.name to check what system we are using, if it is posix we reuse the bound port.
        if os.name == "posix":
            self.serversocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

        self.serverSocket.bind(('',self.portnumber))
        self.serverSocket.listen()

    #We receive a request from our browser that contains att the most 8KiB of data which is the normal standard.
    def GetRequest(self):
        self.connectionSocket, self.addr = self.serverSocket.accept()
        request = self.connectionSocket.recv(8192)
        return request, True

    #Sends message back to the browser.
    def SendBack(self,message):
        self.connectionSocket.send(message)

    #Closes the socket 
    def CloseServer(self):
        self.serverSocket.close()
        self.connectionSocket.close()

