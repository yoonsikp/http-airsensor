#!/usr/bin/env python
#
# Test SDL_Pi_HDC1000
#
# June 2017
#

#imports

import time
import datetime
import SDL_Pi_HDC1000


import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
 
        # Send headers
        if self.path.endswith('temperature'):
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send message back to client
            message = '%3.1f' % (float(hdc1000.readTemperature()))
            # Write content as utf-8 data
            self.wfile.write(bytes(message, 'UTF-8'))
        if self.path.endswith('humidity'):
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send message back to client
            message = '%3.1f' % (float(hdc1000.readHumidity()))
            # Write content as utf-8 data
            self.wfile.write(bytes(message, 'UTF-8'))
        return
# Main Program

hdc1000 = SDL_Pi_HDC1000.SDL_Pi_HDC1000(twi=0)
hdc1000.setTemperatureResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
hdc1000.setHumidityResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT)

def run():
  print('starting server...') 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('', 8080)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()

run()

