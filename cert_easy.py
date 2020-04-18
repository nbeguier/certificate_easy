#!/usr/bin/env python3
"""
Easy use of certificate

Copyright 2017-2020 Nicolas BEGUIER
Licensed under the Apache License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from argparse import ArgumentParser
from sys import argv

# Third party library imports
from ssl import get_server_certificate
from OpenSSL.crypto import load_certificate, FILETYPE_PEM
from OpenSSL.crypto import X509Store, X509StoreContext, X509StoreContextError

# Debug
# from pdb import set_trace as st

VERSION = '1.0.2'

COLORS = {
    'red': '\033[1;31m',
    'green': '\033[1;32m',
    'yellow': '\033[1;33m',
    'purple': '\033[1;34m',
    'pink': '\033[1;35m',
    'light_blue': '\033[1;36m',
    'white': '\033[m',
    'native': '\033[m',
    'bold': '\033[1m'
}

def color_message(message, color_name, bold=False):
    """ Print in a specific color """
    if bold:
        color = "{bold}{color}".format(bold=COLORS['bold'], color=COLORS[color_name])
    else:
        color = COLORS[color_name]
    return "{color}{message}{reset_color}".format(color=color,
                                                  message=message,
                                                  reset_color=COLORS['native'])

def display(cert_path, fqdn=False, extensions=False, port=443):
    """ Display certificate """
    if fqdn:
        st_cert = get_server_certificate((cert_path, port))
    else:
        st_cert = open(cert_path, 'rt').read()
    cert = load_certificate(FILETYPE_PEM, st_cert)

    print(color_message("Common Name: ", "green", bold=True) + cert.get_subject().CN)
    print(color_message("Subject: ", "green", bold=True))
    for subject in cert.get_subject().get_components():
        print(color_message("    {}: ".format(
            subject[0].decode("utf-8")), "bold") + subject[1].decode("utf-8"))

    print(color_message("Issuer: ", "green", bold=True) + cert.get_issuer().CN)
    print(color_message("Validity: ", "bold"))
    print(color_message("    Not Before: ", "bold") + cert.get_notBefore().decode("utf-8"))
    print(color_message("    Not After: ", "bold") + cert.get_notAfter().decode("utf-8"))
    if cert.has_expired():
        print(color_message("Certificate expired", "red"))

    if extensions:
        print(color_message("Signature Algorithm: ", "bold") \
            + cert.get_signature_algorithm().decode("utf-8"))
        print(color_message("X509v3 extensions: ", "bold"))
        for ext_id in range(cert.get_extension_count()):
            print(color_message("    {}: ".format(cert
                                                  .get_extension(ext_id)
                                                  .get_short_name()
                                                  .decode("utf-8")), "bold") +
                  cert.get_extension(ext_id).__str__())

def verify(cert_path, ca_path, fqdn=False, port=443):
    """ Verify a couple of certificate and CA """
    if fqdn:
        st_cert = get_server_certificate((cert_path, port))
    else:
        st_cert = open(cert_path, "rt").read()
    st_ca = open(ca_path, "rt").read()
    cert = load_certificate(FILETYPE_PEM, st_cert)
    ca_cert = load_certificate(FILETYPE_PEM, st_ca)
    store = X509Store()
    store.add_cert(ca_cert)
    store_ctx = X509StoreContext(store, cert)
    try:
        if store_ctx.verify_certificate() is None:
            print(color_message("Verification successful !", "green", bold=True))
    except X509StoreContextError as error:
        print(color_message("Verification error: ", "red", bold=True) + str(error))

def main():
    """
    Main function
    """
    if __name__ == "__main__":
        parser = ArgumentParser()

        subparsers = parser.add_subparsers(help="commands")

        parser.add_argument('--version', action='version', version=VERSION)

        # A display command
        display_parser = subparsers.add_parser("display", help="Display certificate.")
        display_parser.add_argument("--input", "-i", action="store",
                                    help="Certificate path.")
        display_parser.add_argument("--input-fqdn", "-u", action="store",
                                    help="Certificate FQDN.")
        display_parser.add_argument("--extensions", "-e", action="store_true",
                                    default=False, help="Display extensions and signature.")
        display_parser.add_argument("--port", "-p", action="store",
                                    default=443, help="Change HTTPs port.")

        # An verify command
        verify_parser = subparsers.add_parser("verify", help="verifiy couple CA, CERTIFICATE")
        verify_parser.add_argument("--input", "-i", action="store", help="Certificate path.")
        verify_parser.add_argument("--ca", action="store", help="CA path.")
        verify_parser.add_argument("--input-fqdn", "-f", action="store",
                                   help="Certificate FQDN.")
        verify_parser.add_argument("--port", "-p", action="store", help="Change HTTPs port.",
                                   default=443)


        args = parser.parse_args()

        if len(argv) < 2:
            parser.print_usage()
        elif argv[1] == "display":
            if args.input is not None:
                display(args.input, extensions=args.extensions)
            elif args.input_fqdn is not None:
                display(args.input_fqdn, fqdn=True, extensions=args.extensions, port=args.port)
            else:
                display_parser.print_usage()
        elif argv[1] == "verify":
            if args.input is not None and args.ca is not None:
                verify(args.input, args.ca, port=args.port)
            elif args.input_fqdn is not None and args.ca is not None:
                verify(args.input_fqdn, args.ca, fqdn=True, port=args.port)
            else:
                verify_parser.print_usage()

main()
