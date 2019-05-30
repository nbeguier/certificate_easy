#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" Simple HTTPs Server """

# Standard library imports
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

HOST = 'localhost'
PORT = 8443
CERTIFICATE_DIRECTORY = 'ssl_test'

httpd = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket,
    certfile='%s/client.pem' % CERTIFICATE_DIRECTORY,
    keyfile='%s/client.key' % CERTIFICATE_DIRECTORY,
    server_side=True)

print('https://%s:%s/' % (HOST, PORT))

httpd.serve_forever()
