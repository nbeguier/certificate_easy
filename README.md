# Cert Easy

## Prerequisites

### Debian/Ubuntu

```
apt install gnutls-bin python3-pip

pip3 install -r requirements.txt
```

## Usage
```
$ bash gen_ca.sh [--cn <common name>] [-o <o>] [--validity <validity>] [--output <output directory>]
```

```
$ bash gen_certificate.sh [--cn <common name>] [-o <o>] [--validity <validity>] [--output <output directory>]
```


```
$ python cert_easy [-h] {display,verify} ...

positional arguments:
  {display,verify}  commands
    display         Display certificate.
    verify          verifiy couple CA, CERTIFICATE

optional arguments:
  -h, --help        show this help message and exit


# display
usage: cert_easy display [-h] [--input INPUT] [--input-fqdn INPUT_FQDN]
                         [--brief]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Certificate path.
  --input-fqdn INPUT_FQDN, -u INPUT_FQDN
                        Certificate FQDN.
  --brief, -b           Enable brief display.
  --port PORT, -p PORT  Change HTTPs port.

# verify
usage: cert_easy verify [-h] [--input INPUT] [--ca CA] [--input-fqdn INPUT_FQDN]

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
mkdir ssl_perso

# Generating CA
bash gen_ca.sh --output ssl_perso/ --cn "My private CA"

# Generating Certificate
bash gen_certificate.sh --output ssl_perso/ --cn "My private server"

# Display your certificate
python3 cert_easy display --input ssl_perso/server.pem

# Verify couple ca
python3 cert_easy verify --input ssl_perso/server.pem --ca ssl_perso/ca.pem
```

### Display server certificate

```bash
# Display server certificate
python3 cert_easy display --input-fqdn github.com

```


### Verify server certificate (beta)

```bash
# Verify certificate with private ca (should fail)
python cert_easy verify --input-fqdn github.com --ca ssl/ca.pem

# Download github ca
# Extract it in the dump
openssl s_client -showcerts -connect github.com:443 </dev/null

# If you don't pass root CA, it may not work...

```
