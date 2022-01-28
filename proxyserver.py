#!/usr/bin/env python3
import client
import server

class Proxy:
    
    def __init__(self):
        self.myServer = server.Server()
        self.myClient = client.Client()