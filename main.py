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
        print("Request from broswer\n", request)
        headers = parse.make_header_dir(request)
        #Checking if get is for text or image
        #text = parse.check_content_type(headers)
        
        request = parse.parse_request(headers)
        print("------------Connecting to the {}--------------\n".format(headers[b"Host:"]))
        myClient.establish_serverconnection(headers[b"Host:"])
        myClient.sendtoserver(request)
        returmessage = myClient.listentoserver()
        
        ContentType = parse.get_content_type(returmessage)
        print("-------------Recived message from server-----------------\n\n")
        print(returmessage)
        #if text:
        contentnottext = parse.check_content(ContentType)
        if contentnottext:
            returmessage = parse.parse_response(returmessage)
        print("------------Sent back to browser--------------\n\n")
        myServer.sendback(returmessage)
        myClient.close_client()
        myServer.connectionsocket.close()



run()

