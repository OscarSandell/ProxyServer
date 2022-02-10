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
        print("Request from broswer\n\n\n\n\n", request.encode())
        headers = make_header_dir(request)
        #Checking if get is for text or image
        text = parse.check_content_type(headers)
        request = parse.parse_request(headers)
        print("------------Connecting to the {}--------------\n".format(headers["Host"]))
        myClient.establish_serverconnection(headers["Host"])
        myClient.sendtoserver(request)
        returmessage = myClient.listentoserver()

        print("-------------Recived message from server-----------------\n\n")
        #print(returmessage)
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
        if header.find("GET") != -1:
            tmp = header.split()
            value = ""
            for i in range(len(tmp)-1):
                value += tmp[i+1] + " "            
            if len(tmp) > 0:
                temp[tmp[0]] = value[:-1]
        else:
            tmp = header.split(": ")
            value = ""
            for i in range(len(tmp)-1):
                value += tmp[i+1]              
            if len(tmp) > 0:
                temp[tmp[0]] = value
    return temp 


'''
def make_header_dir(req):
    headers = {}
    for line in req.splitlines()[1:]:

        if line == "" or line == "\r":
            break
        else:
            head, value = line.split(": ", 1)
            headers[head] = value

    return headers
'''



run()

