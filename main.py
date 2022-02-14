#!/usr/bin/env python3
import server
import client
import parse
import sys
import os

def run():

    #First we instantiate the server- and the clientobjects of the proxy.
    myServer = server.Server()
    myClient = client.Client()
    
    #Simple code that handles arguments to select a desired port.
    arguments = sys.argv
    if len(arguments) != 2:
        if os.name == "posix":
            print("To few commandline arguments, there should be 2 i.e <./main.py portnumber>")
        elif os.name == "nt":
            print("To few commandline arguments, there should be 2 i.e <main.py portnumber>")
        return
    portNumber = 0
    try:
        portNumber = int(arguments[-1])
        if ((portNumber > 65535) or (portNumber < 0)):
            print("Invalid portnumber, ranges of portnumbers should be between 0 and 65535 yours were = ",portNumber)
            return
    except:
        print("Invalid second argument, can't convert it into a valid portnumber == ",portNumber)
        return
        
    #The server opens the proxyport specified by your commandline and starts listening on it.
    myServer.Listen(portNumber)

    while True:
        proxyToWebServerConnection = False
        browserToProxyConnection = False
        try:
            
            print("////////////////////////////////////////////////////////////////////////////\n\n")
            print("------------Waiting for new request--------------\n")

            #Wait for an incoming connection and opens a socket to the browser and read the socket information. 
            request, browserToProxyConnection  = myServer.GetRequest()
            print("------------Receieved new request--------------\n")

            #Parse headers and put them into a dictionary with the headertitles as key and their information as associated values.
            headers = parse.ParseHeader(request)
            print("---This is the browser request---\n")
            print(request, "\n")
            
            #Sometimes the request is empty so we ignore it. Dunno why but it just happens sometimes when we connect to weird webpages
            if request == b"":
                myClient.CloseClient()
                myServer.connectionSocket.close()
                continue
            host = headers[b"Host:"]

            #If there is an headertiltle called GET we check the header and make apropriate changes to it.
            if (b'GET' in headers):
                request,host, madeChanges = parse.FakeRequest(headers)
                if madeChanges:
                    print("---Sending a faked request---\n")
                    print(request)
                else:
                    print("Found no links to replace, forwarding...\n")
            
            print("------------Connecting to the {}--------------\n".format(host))
            
            #Connect to the webserver using the hostname.
            proxyToWebServerConnection = myClient.EstablishServerConnection(host)

            #Sending the request to the webserver.
            myClient.SendToServer(request)

            #Listening for a response from the webserver.
            headers, message = myClient.ListenToServer()

            #Parsing the headers of the response into a dictionary like before.
            headers = parse.ParseHeader(headers)
            print("-------------Recived message from server-----------------\n")
        
            print("---This is the response header from the server---\n")
            print(headers, "\n")

            #Determen what kind of protocol the webserver is using.
            httpheader = b''
            if b'HTTP/1.1' in headers:
                httpheader = b'HTTP/1.1'
            elif b'HTTP/1.0' in headers:
                httpheader = b'HTTP/1.0'
            if httpheader != b'':
                if b"200" in headers[httpheader]:
                    #Determening the content type so that we dont accidentally try to decode an image.
                    #                   
                    contentIsText = parse.CheckContentType(headers)
                    if contentIsText:
                        
                        #Try to make changes to the response if nessesary.
                        headers, message, madeChanges = parse.FakeResponse(headers,message)
                        if madeChanges:
                            print("Sending back a faked response...\n")
                        else:
                            print("Found no words to replace, forwarding...\n")
                    else:
                        print("Sending back a picture...\n")
                        
            #Reconstructing the headers dictionary into a bytestring again.
            header = parse.ReconstructHeader(headers)
        
            returmessage = header + message
            print("------------Sending back to browser--------------\n")
            
            #Send back the complete response.
            myServer.SendBack(returmessage)  
        except Exception as ex:
            print(ex)
            print("Something went wrong, this request have been dropped\n")
        finally:

            #Close the connection to the webbrowser and the webserver.
            if proxyToWebServerConnection:
                myClient.CloseClient()
            if browserToProxyConnection:
                myServer.connectionSocket.close()
            print("---Finnished rountrip---\n\n")



run()

