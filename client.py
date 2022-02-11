#!/usr/bin/env python3
from socket import *
import time
import parse

class Client:

    
    def __init__(self):
        print("Client Created.")

    def getip(self,argument):
        address = gethostbyname(argument)
        return address

    def establish_serverconnection(self,servername):
        Portnumber = 80
        self.clientsocket = socket(AF_INET,SOCK_STREAM)
        self.clientsocket.connect((self.getip(servername.decode()),Portnumber))
        return True


    def sendtoserver(self,message):
        self.clientsocket.send(message)
    
    
    def estimate_response_size(self,header):
        temp = parse.parse_respons_to_header(header)
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
    
    def listentoserver(self):
        checksize = True
        retur = b''
        sizeofresponse,totalsize,contentSize,headerSize = 0,0,0,0
        while True:
            receive = self.clientsocket.recv(8192)
            
            totalsize += len(receive)
            if not receive:
                break
            if(checksize == True):
                contentSize, headerSize = self.estimate_response_size(receive)
                sizeofresponse = contentSize + headerSize
                checksize = False
            retur += receive
            if(totalsize == sizeofresponse):
                break
        header = retur[0:headerSize]
        message = retur[headerSize:]
        return header, message
    '''
    def listentoserver(self):
        response = b""
        while True:
            receive = self.clientsocket.recv(1024)
            storlek = len(receive)
            print("-----New Recieve of size {}----\n".format(storlek),receive,"\n\n")
            response += receive
            if storlek < 1024:
                break
        
        
        headersize = len(parse.parse_respons_to_header(response))

        header = response[0:headersize]
        message = response[headersize:]
        return header, message
    '''
    def close_client(self):
        self.clientsocket.close()