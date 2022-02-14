#!/usr/bin/env python3
from socket import *
import time
import parse

class Client:

    
    def __init__(self):
        print("Client Created.")

    #Translates hostname into an IP address
    def GetIP(self,argument):
        address = gethostbyname(argument)
        return address

    #Establish a connection with the webserver.
    def EstablishServerConnection(self,serverName):
        Portnumber = 80
        self.clientSocket = socket(AF_INET,SOCK_STREAM)
        self.clientSocket.connect((self.GetIP(serverName.decode()),Portnumber))
        return True

    #Sends message to the webserver.
    def SendToServer(self,message):
        self.clientSocket.send(message)
    
    #Estimates the size of the complete response message.
    #Here we figure out the headersize and messagesize and returns them (assuming Content-Length exists)
    def EstimateResponseSize(self,temp):
        headerSize = len(temp)
        ContentLengthIndex = temp.find(b'Content-Length: ')
        if ContentLengthIndex != -1:
            backSlashrIndex = temp.find(b'\r',ContentLengthIndex)
            if(temp == b''):
                return (0,0)
            contentlength = int(temp[ContentLengthIndex+16:backSlashrIndex].decode())
        else:
            contentlength = 0
        
        return (contentlength,headerSize)
    
    #Listens to the server response.
    def ListenToServer(self):
        retur = b''
        headerFound = False
        sizeOfResponse,totalSize,contentSize,headerSize = 0,0,0,0
        while True:
            receive = self.clientSocket.recv(8192)
            retur += receive
            
            #Check if we have not found the header 
            if (headerFound == False ) and (b"\r\n\r\n" in retur):
                header,headerFound = parse.ParseResponseToHeaders(retur)
                #if we have found the header we want to estimate/calculate the response size
                if headerFound:
                    contentSize, headerSize = self.EstimateResponseSize(header)
                    sizeOfResponse = contentSize + headerSize
            totalSize += len(receive)
            if not receive:
                break
            if(totalSize == sizeOfResponse):
                break
        #We return the header and message separately so that we dont have to search through them when its not neccessary
        header = retur[0:headerSize]
        message = retur[headerSize:]
        return header, message
        
  
    #Closes the socket to the webserver.
    def CloseClient(self):
        self.clientSocket.close()