#!/usr/bin/env python3
from socket import *
import time
import parse

class Client:

    
    def __init__(self):
        print("Client Created.")

    #Translates hostname into an IP address
    def getip(self,argument):
        address = gethostbyname(argument)
        return address

    #Establish a connection with the webserver.
    def establish_serverconnection(self,servername):
        Portnumber = 80
        self.clientsocket = socket(AF_INET,SOCK_STREAM)
        self.clientsocket.connect((self.getip(servername.decode()),Portnumber))
        return True

    #Sends message to the webserver.
    def sendtoserver(self,message):
        self.clientsocket.send(message)
    
    #Estimates the size of the complete response message.
    def estimate_response_size(self,temp):
        #temp = parse.parse_respons_to_header(header)
        headersize = len(temp)
        ContentLengthIndex = temp.find(b'Content-Length: ')
        if ContentLengthIndex != -1:
            backslashrindex = temp.find(b'\r',ContentLengthIndex)
            if(temp == b''):
                return (0,0)
            contentlength = int(temp[ContentLengthIndex+16:backslashrindex].decode())
        else:
            contentlength = 0
        
        return (contentlength,headersize)
    
    #Listens to the server response.
    def listentoserver(self):
        retur = b''
        headerFound = False
        sizeOfResponse,totalSize,contentSize,headerSize = 0,0,0,0
        while True:
            receive = self.clientsocket.recv(8192)
            retur += receive
            
            if (headerFound == False ) and (b"\r\n\r\n" in retur):
                header,headerFound = parse.parse_respons_to_header(retur)
                if headerFound:
                    contentSize, headerSize = self.estimate_response_size(header)
                    sizeOfResponse = contentSize + headerSize
            totalSize += len(receive)
            if not receive:
                break
            if(totalSize == sizeOfResponse):
                break
        header = retur[0:headerSize]
        message = retur[headerSize:]
        return header, message
        
  
    #Closes the socket to the webserver.
    def close_client(self):
        self.clientsocket.close()