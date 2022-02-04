#!/usr/bin/env python3
from socket import *
import os
class Server:

    def __init__(self):
        print("Server Created.")

    def listen(self):
        self.Portnumber = 13000
        self.serversocket = socket(AF_INET,SOCK_STREAM)
        if os.name == "posix":
            print("So reuseaddr")
            self.serversocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.serversocket.bind(('',self.Portnumber))
        self.serversocket.listen(1)

        
        

    def get_request(self):
        self.connectionsocket, self.addr = self.serversocket.accept()
        sentence = self.connectionsocket.recv(4096).decode()
        print(sentence)
        headers = sentence.split("\r\n")
        #Delar upp headers i en dictionary med headernamn som nycklar
        temp = {}
        for header in headers:
            tmp = header.split()
            if len(tmp) > 0:
                temp[tmp[0]] = tmp[1]
        print("printar headers\n\n\n\n"  )
        print(temp)
        return (sentence,temp)

    def sendback(self,message):
        self.connectionsocket.send(message)

    def close_server(self):
        self.serversocket.close()
        self.connectionsocket.close()

