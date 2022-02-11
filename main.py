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
        headers = parse.parse_header(request)
        print(request)
        if request == b"":
            myClient.close_client()
            myServer.connectionsocket.close()
            continue
        host = headers[b"Host:"]
        
        if (b'GET' in headers) or (b'HTTP/' in headers):  
            request,host = parse.fake_request(headers)
        print("------------Connecting to the {}--------------\n".format(host))
        myClient.establish_serverconnection(host)
        myClient.sendtoserver(request)
        headers, message = myClient.listentoserver()
        headers = parse.parse_header(headers)
        contentType = parse.get_content_type(headers)
        print("-------------Recived message from server-----------------\n\n")
        if b'HTTP/' in headers:
            if b"200" in headers[b"HTTP/"]:                  
                contentText = parse.check_content(contentType)
                if contentText:
                    headers, message = parse.fake_response(headers,message)  

        headers = parse.reconstruct_headers(headers)
        returmessage = headers + message
        
        print("------------Sent back to browser--------------\n\n")
        myServer.sendback(returmessage)
        myClient.close_client()
        myServer.connectionsocket.close()



run()

