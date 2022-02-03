#!/usr/bin/env python3
from socket import *
#from socket import gethostbyname as ghbn
import time

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
        retur = b''
        tic = time.perf_counter()
        while True:
            receive = self.clientsocket.recv(1)
            if not receive:
                break
            retur += receive
        toc = time.perf_counter()
        print(f"Fyllde strängen på {toc - tic:0.4f} sekunder")

        retur = retur.decode('utf-8')
        print(retur)
        return retur.encode()
    
    def close_client(self):
        self.clientsocket.close()