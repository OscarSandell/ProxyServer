#!/usr/bin/env python3
from socket import *
import time
import parse

class Client:

    
    def __init__(self):
        print("Client Created.")

    def getip(self,argument):
        address = gethostbyname(argument)
        #print(address)
        return address

    def establish_serverconnection(self,servername):
        Portnumber = 80
        self.clientsocket = socket(AF_INET,SOCK_STREAM)
        self.clientsocket.connect((self.getip(servername.decode()),Portnumber))


    def sendtoserver(self,message):
        #print("Skickade:\n\n",message)
        ##print("Encodat\n\n")
        ##print(message.encode())
        self.clientsocket.send(message)
        #print("Request sent...\n")
    
    def estimate_response_size(self,header):
        temp = parse.parse_respons_to_header(header)
        headersize = len(temp)
        #print(temp)
        ContentLengthIndex = temp.find(b'Content-Length: ')
        backslashrindex = temp.find(b'\r',ContentLengthIndex)
        #print("DETTA ÄR \/R : \n",temp[backslashrindex])
        contentlength = int(temp[ContentLengthIndex+16:backslashrindex].decode())
        #print("Contentlength = ",contentlength)
        #print("Content lengthindex: ",ContentLengthIndex)
        #totalsize = headersize + contentlength
        ##print("Totalsize= " + str(totalsize) )
        
        return (contentlength,headersize)

    def listentoserver(self):
        checksize = True
        retur = b''
        sizeofresponse = 0
        totalsize = 0
        header = b''
        message = b''
        contentSize = 0
        headerSize = 0
        while True:
            receive = self.clientsocket.recv(8192)
            totalsize += len(receive)
            if(checksize == True):
                contentSize, headerSize = self.estimate_response_size(receive)
                sizeofresponse = contentSize + headerSize
                checksize = False
            if not receive:
                break
            retur += receive
            if(totalsize == sizeofresponse):
                break
        header = retur[0:headerSize]
        message = retur[headerSize:]
        ##print("Checkar så att size of header och message = sizeofresponse: {} + {} == {} ".format(len(header),len(message),sizeofresponse))
        return header, message


    def close_client(self):
        self.clientsocket.close()