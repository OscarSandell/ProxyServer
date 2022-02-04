#!/usr/bin/env python3
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
        request, headers = myServer.get_request()
        text = parse.check_content_type(headers)
        host = headers[1].split()[1]
        if "linkopings_slotts-_och_domkyrkoomrade.jpg" in request:
            host = "visitlinkoping.se"
        myClient.establish_serverconnection(host)
        myClient.sendtoserver(request)
        returmessage = myClient.listentoserver()
        if text:
            returmessage = parse.parse_response(returmessage.decode()).encode()
        myServer.sendback(returmessage)
        myClient.close_client()


run()



