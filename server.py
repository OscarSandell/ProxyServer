#!/usr/bin/env python3
from socket import *
import os
class Server:

    def __init__(self):
        print("Server Created.")

    #Takes portnumber as argument and binds the port to a TCP socket, we are using ipv4 
    def listen(self,portnumber):
        self.Portnumber = portnumber
        self.serversocket = socket(AF_INET,SOCK_STREAM)
        if os.name == "posix":
            self.serversocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.serversocket.bind(('',self.Portnumber))
        self.serversocket.listen()

    #We receeive a request from our browser that contains att the most 8KiB of data which is the normal standard
    def get_request(self):
        self.connectionsocket, self.addr = self.serversocket.accept()
        request = self.connectionsocket.recv(8192)
        return request, True

    #Sends message back to the browser.
    def sendback(self,message):
        self.connectionsocket.send(message)

    #Closes the socket 
    def close_server(self):
        self.serversocket.close()
        self.connectionsocket.close()

