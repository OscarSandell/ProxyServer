#!/usr/bin/env python3
from email import header
from tarfile import HeaderError
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
        request, headers = myServer.get_request()
        text = parse.check_content_type(headers)
        if "imagevault/publishedmedia/p1j0ds7hsi1adv0qqi3e/Toppbild-startsida-stadsvy.jpg" in request:
            headers["GET"] = "https://www.linkoping.se/imagevault/publishedmedia/p1j0ds7hsi1adv0qqi3e/Toppbild-startsida-stadsvy.jpg"
            headers["Host:"] = "linkoping.se"
        myClient.establish_serverconnection(headers["Host:"])
        temp = ""
        for key,item in headers.items():
            temp += key + " " + item + "\r\n"
        print("this is temp \n\n\n" + temp)
        myClient.sendtoserver(request)
        returmessage = myClient.listentoserver()
        if text:
            returmessage = parse.parse_response(returmessage.decode()).encode()
        myServer.sendback(returmessage)
        myClient.close_client()


run()
'''
def insert_new_link(headers):
    
    for header in headers:
        
    if "http://zebroid.ida.liu.se/fakenews/Stockholm-spring.jpg" in headers[0]:

'''
