#!/usr/bin/env python3
import server
import client
import proxyserver

#message , adress = server.listen()
#print(message)
#print(adress)
#client.send(message,adress.split()[1])

proxy = proxyserver.Proxy()

message, adress = proxy.myServer.listen()
print(message)
print(adress)
print("Nu ska vi skicka till servern \n")
returmessage = proxy.myClient.sendtoserver(message,adress.split()[1])
print("\n\n\n" + returmessage.decode())


proxy.myServer.sendback(returmessage)

proxy.myServer.close_server()
proxy.myClient.close_client()