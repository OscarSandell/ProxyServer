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
        if "wp-content/uploads/2016/04/Linkopingskontoret-600x600.jpg" in request:
            headers["GET"] = "https://www.glimstedt.se/wp-content/uploads/2016/04/Linkopingskontoret-600x600.jpg"
            headers["Host:"] = "glimstedt.se"
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
