#!/usr/bin/env python3
from socket import *
import time

class Client:

    
    def __init__(self):
        print("Client Created.")

    def getip(self,argument):
        address = gethostbyname(argument)
        print(address)
        return address

    def establish_serverconnection(self,servername):
        Portnumber = 80
        self.clientsocket = socket(AF_INET,SOCK_STREAM)
        self.clientsocket.connect((self.getip(servername),Portnumber))


    def sendtoserver(self,message):
        self.clientsocket.send(message.encode())
    
    def listentoserver(self):
        retur = b''
        while True:
            receive = self.clientsocket.recv(1)
            if not receive:
                break
            retur += receive
        return retur

    def close_client(self):
        self.clientsocket.close()