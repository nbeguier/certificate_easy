#!/usr/bin/env python3
"""
Generate CA

Copyright 2017-2022 Nicolas BEGUIER
Licensed under the Apache License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from argparse import ArgumentParser
from random import randint

# Third party library imports
from OpenSSL import crypto

VERSION = '1.0.1'

def create_ca(output_directory, common_name, validity):
    """
    Create CA main funtion
    """
    ca_key = crypto.PKey()
    ca_key.generate_key(crypto.TYPE_RSA, 4096)

    ca_cert = crypto.X509()
    ca_cert.set_version(2)
    ca_cert.set_serial_number(randint(50000000, 100000000))

    ca_subj = ca_cert.get_subject()
    ca_subj.commonName = common_name

    ca_cert.set_issuer(ca_subj)
    ca_cert.set_pubkey(ca_key)

    ca_cert.add_extensions([
        crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=ca_cert),
    ])

    ca_cert.add_extensions([
        crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid:always,issuer",
                             issuer=ca_cert),
    ])

    ca_cert.add_extensions([
        crypto.X509Extension(b"basicConstraints", True, b"CA:TRUE"),
        crypto.X509Extension(b"keyUsage", True, b"digitalSignature, keyCertSign, cRLSign"),
    ])


    ca_cert.gmtime_adj_notBefore(0)
    ca_cert.gmtime_adj_notAfter(int(validity))

    ca_cert.sign(ca_key, "sha256")

    # Save certificate
    with open("%s/ca.pem" % output_directory, "w") as ca_cert_file:
        ca_cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, ca_cert).decode("utf-8"))

    # Save private key
    with open("%s/ca.key" % output_directory, "w") as ca_key_file:
        ca_key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key).decode("utf-8"))

if __name__ == "__main__":
    PARSER = ArgumentParser()

    PARSER.add_argument('--version', action='version', version=VERSION)

    PARSER.add_argument("--output", "-o", action="store",
                        help="Output directory.",
                        default="ssl/")
    PARSER.add_argument("--cn", action="store",
                        help="Common name.",
                        default="Root CA")
    PARSER.add_argument("--validity", "-v", action="store",
                        help="Validity.",
                        default=365*24*60*60)

    ARGS = PARSER.parse_args()

    create_ca(ARGS.output, ARGS.cn, ARGS.validity)
