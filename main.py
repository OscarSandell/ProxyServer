#!/usr/bin/env python3
import http
import server
import client
import parse




def run():

    myServer = server.Server()
    myClient = client.Client()
    myServer.listen()

    while True:
        proxyToWebServerConnection = False
        browserToProxyConnection = False
        try:
            
            print("////////////////////////////////////////////////////////////////////////////\n\n")
            print("------------Waiting for new request--------------\n")
            request, browserToProxyConnection  = myServer.get_request()
            print("------------Receieved new request--------------\n")
            headers = parse.parse_header(request)
            print("---This is the browser request---\n")
            print(request, "\n")
            if request == b"":
                myClient.close_client()
                myServer.connectionsocket.close()
                continue
            host = headers[b"Host:"]
        
            if (b'GET' in headers):
                request,host, madeChanges = parse.fake_request(headers)
                if madeChanges:
                    print("---Sending a faked request---\n")
                    print(request)
                else:
                    print("Found no links to replace, forwarding...\n")
            
            print("------------Connecting to the {}--------------\n".format(host))
            proxyToWebServerConnection = myClient.establish_serverconnection(host)
            myClient.sendtoserver(request)
            headers, message = myClient.listentoserver()
            headers = parse.parse_header(headers)
            contentType = parse.get_content_type(headers)
            print("-------------Recived message from server-----------------\n")
        
            print("---This is the response header from the server---\n")
            print(headers, "\n")

            httpheader = b''
            if b'HTTP/1.1' in headers:
                httpheader = b'HTTP/1.1'
            elif b'HTTP/1.0' in headers:
                httpheader = b'HTTP/1.0'
            if httpheader != b'':
                if b"200" in headers[httpheader]:                  
                    contentText = parse.check_content(contentType)
                    if contentText:
                        headers, message, madeChanges = parse.fake_response(headers,message)
                        if madeChanges:
                            print("Sending back a faked response...\n")
                        else:
                            print("Found no words to replace, forwarding...\n")
                    else:
                        print("Sending back a picture...\n")

            headers = parse.reconstruct_headers(headers)
        
            returmessage = headers + message
            print("------------Sending back to browser--------------\n")
            myServer.sendback(returmessage)  
        except:
            #Gör något
            print("Something went wrong, this request have been dropped\n")
        finally:
            if proxyToWebServerConnection:
                myClient.close_client()
            if browserToProxyConnection:
                myServer.connectionsocket.close()
            print("---Finnished rountrip---\n\n")



run()

