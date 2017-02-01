#!/bin/bash

CA_CN='TestCA'
# The organization of the subject.
CA_O='AutoSign'
# The country of the subject. Two letter code.
CA_C='FR'
# In how many days, counting from today, this certificate will expire.
CA_VALIDITY=365
CA_TEMPLATE=.ca.tmp

# Génération de la clé privée de la CA
openssl req -x509 -newkey rsa:4096 -keyout ca.key -nodes -subj "/CN=${CA_CN}/O=${CA_O}/C=${CA_C}"

# Création du template CA
echo "
organization = ${CA_O}
country = ${CA_C}
cn = ${CA_CN}
expiration_days = ${CA_VALIDITY}
ca
cert_signing_key
crl_signing_key" > ${CA_TEMPLATE}

# Génération de la CA
certtool --generate-self-signed --load-privkey ca.key --template ${CA_TEMPLATE} --outfile ca.pem

rm ${CA_TEMPLATE}