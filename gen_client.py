#!/usr/bin/env python3
"""
Generate Client

Copyright 2017 Nicolas BEGUIER
Licensed under the Apache License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from argparse import ArgumentParser
from random import randint

# Third party library imports
from OpenSSL import crypto

VERSION = '1.0.1'

def create_cert(ca_cert, ca_subj, ca_key, arguments):
    """
    Create Certificate main funtion
    """

    client_key = crypto.PKey()
    client_key.generate_key(crypto.TYPE_RSA, 4096)

    client_cert = crypto.X509()
    client_cert.set_version(2)
    client_cert.set_serial_number(randint(50000000, 100000000))

    client_subj = client_cert.get_subject()
    client_subj.commonName = arguments["common_name"]
    client_cert.set_issuer(ca_subj)
    client_cert.set_pubkey(client_key)

    client_cert.add_extensions([
        crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
    ])

    client_cert.add_extensions([
        crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid", issuer=ca_cert),
        crypto.X509Extension(b"extendedKeyUsage", False, b"serverAuth"),
        crypto.X509Extension(b"keyUsage", True, b"digitalSignature, keyEncipherment"),
    ])

    client_cert.add_extensions([
        crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=client_cert),
    ])
    client_cert.gmtime_adj_notBefore(0)
    client_cert.gmtime_adj_notAfter(int(arguments["validity"]))

    client_cert.sign(ca_key, "sha256")

    # Save certificate
    with open("%s/client.pem" % arguments["output_directory"], "w") as client_cert_file:
        client_cert_file.write(
            crypto.dump_certificate(crypto.FILETYPE_PEM, client_cert).decode("utf-8"))

    # Save private key
    with open("%s/client.key" % arguments["output_directory"], "w") as client_key_file:
        client_key_file.write(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, client_key).decode("utf-8"))


if __name__ == "__main__":
    PARSER = ArgumentParser()

    PARSER.add_argument('--version', action='version', version=VERSION)

    PARSER.add_argument("--output", "-o", action="store",
                        help="Output directory.",
                        default="ssl/")
    PARSER.add_argument("--cn", action="store",
                        help="Common name.",
                        default="localhost")
    PARSER.add_argument("--validity", "-v", action="store",
                        help="Validity.",
                        default=365*24*60*60)

    ARGS = PARSER.parse_args()

    KEY_PATH = "{}/ca.key".format(ARGS.output)
    ROOT_CA_PATH = "{}/ca.pem".format(ARGS.output)

    with open(KEY_PATH, "r") as key_path_file:
        PRIVATE_KEY = crypto.load_privatekey(crypto.FILETYPE_PEM, key_path_file.read())

    with open(ROOT_CA_PATH, "r") as root_ca_path_file:
        CA_CERT = crypto.load_certificate(crypto.FILETYPE_PEM, root_ca_path_file.read())

    SUBJECT = CA_CERT.get_subject()

    create_cert(CA_CERT, SUBJECT, PRIVATE_KEY,
                {
                    "common_name": ARGS.cn,
                    "validity": ARGS.validity,
                    "output_directory": ARGS.output
                })
