#!/usr/bin/env python3
#-*- coding: utf-8 -*-
""" Simple HTTPs Server """

# Standard library imports
from __future__ import absolute_import
from http.server import HTTPServer, SimpleHTTPRequestHandler
from ssl import wrap_socket

HOST = "localhost"
PORT = 8443
CERTIFICATE_DIRECTORY = "ssl_test"

httpd = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
httpd.socket = wrap_socket (httpd.socket,
    certfile="{}/client.pem".format(CERTIFICATE_DIRECTORY),
    keyfile="{}/client.key".format(CERTIFICATE_DIRECTORY),
    server_side=True)

print("https://{host}:{port}/".format(host=HOST, port=PORT))

httpd.serve_forever()
