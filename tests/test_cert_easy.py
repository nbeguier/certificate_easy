#!/usr/bin/env python3
"""
Tests cert_easy

Copyright 2017-2023 Nicolas BEGUIER
Licensed under the Apache License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
import os
import sys

# Third party library imports
import pytest

# Own library
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')
import cert_easy

# Debug
# from pdb import set_trace as st

def test_display_cert_path(capsys):
    cert_easy.display('ssl/client.pem', extensions=True)
    out, err = capsys.readouterr()
    assert err == ''
    assert 'Common Name: \x1b[mlocalhost\n' in out
    assert 'CN: \x1b[mlocalhost\n' in out
    assert 'Not Before: \x1b[m2020-03-29 13:46:14\n' in out
    assert 'Not After: \x1b[m2051-12-06 15:32:53\n' in out
    assert 'Signature Algorithm' in out
    cert_easy.display('ssl/client_expired.pem')
    out, err = capsys.readouterr()
    assert err == ''
    assert 'Certificate expired' in out

def test_display_cert_fqdn(capsys):
    cert_easy.display('github.com', fqdn=True)
    out, err = capsys.readouterr()
    assert err == ''
    assert 'Common Name: \x1b[mgithub.com\n' in out

def test_verify_cert_path(capsys):
    cert_easy.verify('ssl/client.pem', 'ssl/ca.pem')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '\x1b[1m\x1b[1;32mVerification successful !\x1b[m\n'
    cert_easy.verify('ssl/client_expired.pem', 'ssl/ca.pem')
    out, err = capsys.readouterr()
    assert err == ''
    assert 'Verification error' in out

def test_verify_cert_fqdn(capsys):
    cert_easy.verify('github.com', 'ssl/ca.pem', fqdn=True)
    out, err = capsys.readouterr()
    assert err == ''
    assert "\x1b[1m\x1b[1;31mVerification error: \x1b[munable to get local issuer certificate\n" in out
