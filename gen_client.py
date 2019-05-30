#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" Generate Client """

# Standard library imports
from argparse import ArgumentParser
import random

# Third party library imports
from OpenSSL import crypto

def create_cert(ca_cert, ca_subj, ca_key, common_name, validity, output_directory):
    client_key = crypto.PKey()
    client_key.generate_key(crypto.TYPE_RSA, 4096)

    client_cert = crypto.X509()
    client_cert.set_version(2)
    client_cert.set_serial_number(random.randint(50000000, 100000000))

    client_subj = client_cert.get_subject()
    client_subj.commonName = common_name
    client_cert.set_issuer(ca_subj)
    client_cert.set_pubkey(client_key)

    client_cert.add_extensions([
        crypto.X509Extension(b'basicConstraints', False, b'CA:FALSE'),
    ])

    client_cert.add_extensions([
        crypto.X509Extension(b'authorityKeyIdentifier', False, b'keyid', issuer=ca_cert),
        crypto.X509Extension(b'extendedKeyUsage', False, b'serverAuth'),
        crypto.X509Extension(b'keyUsage', True, b'digitalSignature, keyEncipherment'),
    ])

    client_cert.add_extensions([
        crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash', subject=client_cert),
    ])
    client_cert.gmtime_adj_notBefore(0)
    client_cert.gmtime_adj_notAfter(int(validity))

    client_cert.sign(ca_key, 'sha256')

    # Save certificate
    with open('%s/client.pem' % output_directory, 'w') as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, client_cert).decode('utf-8'))

    # Save private key
    with open('%s/client.key' % output_directory, 'w') as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, client_key).decode('utf-8'))


if __name__ == '__main__':
    PARSER = ArgumentParser()

    PARSER.add_argument('--output', '-o', action='store',
                        help='Output directory.',
                        default='ssl/')
    PARSER.add_argument('--cn', action='store',
                        help='Common name.',
                        default='localhost')
    PARSER.add_argument('--validity', '-v', action='store',
                        help='Validity.',
                        default=365*24*60*60)

    ARGS = PARSER.parse_args()

    key_path = '%s/ca.key' % ARGS.output
    root_ca_path = '%s/ca.pem' % ARGS.output

    with open(key_path, 'r') as f:
        private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())

    with open(root_ca_path, 'r') as f:
        ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())

    subject = ca_cert.get_subject()

    create_cert(ca_cert, subject, private_key, ARGS.cn, ARGS.validity, ARGS.output)
