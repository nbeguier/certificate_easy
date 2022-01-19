#!/usr/bin/env python3
"""
Simple HTTPs Server

Copyright 2017-2022 Nicolas BEGUIER
Licensed under the Apache License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from http.server import HTTPServer, SimpleHTTPRequestHandler
from ssl import wrap_socket

HOST = "localhost"
PORT = 8443
CERTIFICATE_DIRECTORY = "ssl_test"

HTTPD = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
HTTPD.socket = wrap_socket(HTTPD.socket,
                           certfile="{}/client.pem".format(CERTIFICATE_DIRECTORY),
                           keyfile="{}/client.key".format(CERTIFICATE_DIRECTORY),
                           server_side=True)

print("https://{host}:{port}/".format(host=HOST, port=PORT))

HTTPD.serve_forever()
