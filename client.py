#!/usr/bin/env python3
from socket import *
import time
import parse

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
        print("Skickade:\n\n",message)
        #print("Encodat\n\n")
        #print(message.encode())
        self.clientsocket.send(message)
        print("Request sent...\n")
    
    def getsize(self,header):
        temp = parse.parse_respons_to_header(header)
        size = len(temp)
        print(temp)
        ContentLengthIndex = temp.find(b'Content-Length: ')
        backslashrindex = temp.find(b'\r',ContentLengthIndex)
        print("DETTA ÄR \/R : \n",temp[backslashrindex])
        contentlength = temp[ContentLengthIndex+16:backslashrindex].decode()
        print("Contentlength = " + contentlength)
        print("Content lengthindex: " + str(ContentLengthIndex))
        totalsize = size + int(contentlength)
        print("Totalsize= " + str(totalsize) )
        return totalsize

    def listentoserver(self):
        checksize = True
        retur = b''
        size = 0
        totalsize = 0
        while True:
            receive = self.clientsocket.recv(8192)
            totalsize += len(receive)
            if(checksize == True):
                size = self.getsize(receive)
                checksize = False
            if not receive:
                break
            retur += receive
            if(totalsize == size):
                break
        return retur


    def close_client(self):
        self.clientsocket.close()