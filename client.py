#!/usr/bin/env python3
from ast import Bytes
from http import client
from socket import *
#from socket import gethostbyname as ghbn


class Client:

    
    def __init__(self):
        print("Client Created.")

    def getip(self,argument):
        address = gethostbyname(argument)
        print(address)
        return address

    def sendtoserver(self,message, servername):
        Portnumber = 80
        self.clientsocket = socket(AF_INET,SOCK_STREAM)
        self.clientsocket.connect((self.getip(servername),Portnumber))
        self.clientsocket.send(message.encode())
        retur = ''
        while True:
            receive = self.clientsocket.recv(1024)
            if receive == '':
                break
            retur += receive.decode()
            print(retur)
        print("Skickat")
        print(retur)
        return retur.encode()
    
    def close_client(self):
        self.clientsocket.close()