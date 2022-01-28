#!/usr/bin/env python3
from socket import *



class Server:

    def __init__(self):
        print("Server Created.")

    def listen(self):
        self.Portnumber = 13000
        self.serversocket = socket(AF_INET,SOCK_STREAM)
        self.serversocket.bind(('',self.Portnumber))
        self.serversocket.listen(1)
        print("Väntar på anslutning")
        self.connectionsocket, self.addr = self.serversocket.accept()
        sentence = self.connectionsocket.recv(2048).decode()
        print(sentence)
        headers = sentence.split("\r\n")
        print(headers)
        print("printar sentence: " + sentence)
        print("printar headers: " + headers[1])
        return (sentence,headers[1])

    def sendback(self,message):
        self.connectionsocket.send(message)

    def close_server(self):
        self.serversocket.close()
        self.connectionsocket.close()


    

