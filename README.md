# Cert Easy

[![Build Status](https://travis-ci.com/nbeguier/certificate_easy.svg?branch=master)](https://travis-ci.com/nbeguier/certificate_easy) [![Python 3.6|3.9](https://img.shields.io/badge/python-3.6|3.9-green.svg)](https://www.python.org/) [![License](https://img.shields.io/github/license/nbeguier/certificate_easy?color=blue)](https://github.com/nbeguier/certificate_easy/blob/master/LICENSE)

Certificate reader and creater via CLI

## Prerequisites

### Debian/Ubuntu

```
apt install python3-pip

pip3 install -r requirements.txt
```

### MacOS

```
brew install python3

pip3 install -r requirements.txt
```

## Usage
```
$ python3 gen_ca.py --help
usage: gen_ca.py [-h] [--version] [--output OUTPUT] [--cn CN] [--validity VALIDITY]

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --output OUTPUT, -o OUTPUT
                        Output directory.
  --cn CN               Common name.
  --validity VALIDITY, -v VALIDITY
                        Validity.
```

```
$ python3 gen_client.py --help
usage: gen_client.py [-h] [--version] [--output OUTPUT] [--cn CN] [--validity VALIDITY]

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --output OUTPUT, -o OUTPUT
                        Output directory.
  --cn CN               Common name.
  --validity VALIDITY, -v VALIDITY
                        Validity.
```


```
$ python3 cert_easy.py --help
usage: cert_easy.py [-h] [--version] {display,verify} ...

positional arguments:
  {display,verify}  commands
    display         Display certificate.
    verify          verifiy couple CA, CERTIFICATE

optional arguments:
  -h, --help        show this help message and exit
  --version         show program's version number and exit


$ python3 cert_easy.py display --help
usage: cert_easy.py display [-h] [--input INPUT] [--input-fqdn INPUT_FQDN] [--extensions] [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Certificate path.
  --input-fqdn INPUT_FQDN, -u INPUT_FQDN
                        Certificate FQDN.
  --extensions, -e      Display extensions and signature.
  --port PORT, -p PORT  Change HTTPs port.


$ python3 cert_easy.py verify --help
usage: cert_easy.py verify [-h] [--input INPUT] [--ca CA] [--input-fqdn INPUT_FQDN] [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Certificate path.
  --ca CA               CA path.
  --input-fqdn INPUT_FQDN, -f INPUT_FQDN
                        Certificate FQDN.
  --port PORT, -p PORT  Change HTTPs port.
```

## Examples

### Generate own certificate

```bash
# Generate certificate
mkdir ssl_test

# Generating CA
python3 gen_ca.py --output ssl_test/

# Generating Certificate
python3 gen_client.py --output ssl_test/

# Display your certificate
python3 cert_easy.py display --input ssl_test/client.pem

# Verify couple ca
python3 cert_easy.py verify --input ssl_test/client.pem --ca ssl_test/ca.pem
```

### Display server certificate

```bash
# Display server certificate
python3 cert_easy.py display --input-fqdn github.com
```


### Test certificate in a local HTTPS server

```bash
# Start HTTPS Server
python3 simple_https_server.py & 

# Should fail (000)
curl -s -o /dev/null -w "%{http_code}\n" https://localhost:8443/

# Sould be a sucess (200)
curl -s -o /dev/null -w "%{http_code}\n" https://localhost:8443/ --cacert ssl_test/ca.pem

# Verify CA
python3 cert_easy.py verify --input-fqdn localhost --port 8443 --ca ssl_test/ca.pem
```


### Verify server certificate

```bash
# Verify certificate with private ca (should fail)
python3 cert_easy.py verify --input-fqdn github.com --ca ssl/ca.pem

# Download github ca
# Extract it in the dump
openssl s_client -showcerts -connect github.com:443 </dev/null

# If you don't pass root CA, it may not work...
```

# License
Licensed under the [Apache License](https://github.com/nbeguier/certificate_easy/blob/master/LICENSE), Version 2.0 (the "License").

# Copyright
Copyright 2017-2022 Nicolas BEGUIER; ([nbeguier](https://beguier.eu/nicolas/) - nicolas_beguier[at]hotmail[dot]com)
