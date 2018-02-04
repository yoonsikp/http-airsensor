#!/usr/bin/env python
#
# Test SDL_Pi_HDC1000
#
# June 2017
#

#imports

import time
import datetime
import g3
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
# HTTPRequestHandler class
cachetime = 0
cache=[-1,-1,-1,-1,-1,-1]

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
  # GET
    def do_GET(self):
        global cachetime
        global cache
        if int(time.time()) - cachetime > 3 or (cache == [-1,-1,-1,-1,-1,-1]):
            cache=air.read("/dev/ttyS1")
            print(cache)
            cachetime = int(time.time())
            print("cache successfuly purged!")
        # Send response status code
        self.send_response(200)
 
        # Send headers
        if self.path.endswith('pm1'):
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send message back to client
            message = str(cache[3])
            # Write content as utf-8 data
            self.wfile.write(bytes(message, 'UTF-8'))
        if self.path.endswith('pm2'):
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send message back to client
            message = str(cache[4])
            # Write content as utf-8 data
            self.wfile.write(bytes(message, 'UTF-8'))
        if self.path.endswith('pm10'):
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send message back to client
            message = str(cache[5])
            # Write content as utf-8 data
            self.wfile.write(bytes(message, 'UTF-8'))
        if self.path.endswith('aq'):
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send message back to client
            message = '1'
            if (cache[4] == -1):
                message = '0'
            if (cache[4] > 15):
                message = '2'
            if (cache[4] > 25):
                message = '3'
            if (cache[5] > 40):
                message = '4'
            if (cache[5] > 65):
                message = '5'
            # Write content as utf-8 data
            self.wfile.write(bytes(message, 'UTF-8'))
        return
# Main Program

air = g3.g3sensor()

def run():
  print('starting server...') 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()

run()
