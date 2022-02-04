#!/usr/bin/env python3
from email import header
from tarfile import HeaderError
from wsgiref import headers
import server
import client
import parse
import socket
import threading
def run():

    myServer = server.Server()
    myClient = client.Client()
    myServer.listen()

    while True:
        print("------------Making new request--------------")
        request = myServer.get_request()
        headers = make_header_dir(request)
        text = parse.check_content_type(headers)
        myClient.establish_serverconnection(headers["Host:"])
        myClient.sendtoserver(request)
        returmessage = myClient.listentoserver()
        if text:
            returmessage = parse.parse_response(returmessage.decode()).encode()
        myServer.sendback(returmessage)
        myClient.close_client()
        myServer.connectionsocket.close()

def make_header_dir(headers):
    headers = headers.split("\r\n")
        #Delar upp headers i en dictionary med headernamn som nycklar
    temp = {}
    for header in headers:
        tmp = header.split()
        if len(tmp) > 0:
            temp[tmp[0]] = tmp[1]
    print("printar headers\n\n\n\n"  )
    print(temp)
    return temp 

run()