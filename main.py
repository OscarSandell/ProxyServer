#!/usr/bin/env python3
import server
import client
import parse
def run():

    myServer = server.Server()
    myClient = client.Client()
    myServer.listen()

    while True:
        print("------------Waiting for new request--------------\n")
        request = myServer.get_request()
        print("------------Receieved new request--------------\n")
        print(request)
        headers = make_header_dir(request)
        #Checking if get is for text or image
        text = parse.check_content_type(headers)
        print("------------Connecting to the {}--------------\n".format(headers["Host:"]))
        myClient.establish_serverconnection(headers["Host:"])
        myClient.sendtoserver(request)
        returmessage = myClient.listentoserver()
        if text:
            returmessage = parse.parse_response(returmessage.decode()).encode()
        print("------------Sent back to browser--------------\n\n")
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
    return temp 

run()