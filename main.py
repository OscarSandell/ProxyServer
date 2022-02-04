#!/usr/bin/env python3
import server
import client
import proxyserver
import parse
import socket

def run():
    proxy = proxyserver.Proxy()
    message, adress = proxy.myServer.listen()

    print("HEJ")
    print(message)
    print(adress)
    print("Nu ska vi skicka till servern \n")
    returmessage = proxy.myClient.sendtoserver(message,adress.split()[1])
#print("\n\n\n" + returmessage.decode())
    returmessage = parse.parse_response(returmessage.decode()).encode()
    print("Returmessage i main.py\n" + returmessage.decode())
    proxy.myServer.sendback(returmessage)
    proxy.myServer.close_server()
    proxy.myClient.close_client()

run()