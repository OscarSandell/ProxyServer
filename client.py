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
        print("Skickade:\n\n" + message)
        print("Encodat\n\n")
        print(message.encode())
        self.clientsocket.send(message.encode())
        print("Request sent...\n")
    
    def getsize(self,header):
        lalal = bytes(header)
        index = lalal.rfind(b"\r\n\r\n") +4 
        temp = lalal[0:index]
        size = len(temp)
        print(temp)
        ContentLengthIndex = temp.find(b'Content-Length: ')
        backslashrindex = temp.find(b'\r',ContentLengthIndex)
        contentlength = temp[ContentLengthIndex+16:backslashrindex].decode()
        print("Contentlength = " + contentlength)
        print("Content lengthindex: " + str(ContentLengthIndex))
        print(index)
        totalsize = size + int(contentlength)
        print("Totalsize= " + str(totalsize) )
        return totalsize

    '''def listentoserver(self):
        try:
            counter = 0
            retur = b''
            size = 0
            #self.clientsocket.settimeout(30.0)
            totalsize = 0
            while True:
                receive = self.clientsocket.recv(8192)
                totalsize += len(receive)
                if(counter < 1):
                    size = self.getsize(receive)
                if (not receive) or (totalsize == size):
                    break
                retur += receive
                print(counter)
                counter += 1
            #print("Lämna loopen")
        #except timeout:
        except:
            print("Timeout")
        return retur'''

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