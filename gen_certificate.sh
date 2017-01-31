#!/bin/bash

CA_CN='TestCA'
# The organization of the subject.
CA_O='AutoSign'
# The country of the subject. Two letter code.
CA_C='FR'
# In how many days, counting from today, this certificate will expire.
CA_VALIDITY=365
CA_TEMPLATE=.ca.tmp

SRV_CN='nicolas.bluesbox.net'
SRV_O='AutoSign'
SRV_C='FR'
SRV_VALIDITY=364
SRV_TEMPLATE=.srv.tmp

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

# Génération de la clé privée du serveur
openssl req -x509 -newkey rsa:4096 -keyout server.key -nodes -subj "/CN=${SRV_CN}/O=${SRV_O}/C=${SRV_C}"

# Création du template serveur
echo "
organization = ${SRV_O}
country = ${SRV_C}
cn = ${SRV_CN}
expiration_days = ${SRV_VALIDITY}
signing_key
encryption_key
tls_www_server
code_signing_key
ocsp_signing_key
time_stamping_key
email_protection_key
ipsec_ike_key" > ${SRV_TEMPLATE}

# # Génération du certificat du serveur
certtool --generate-certificate --template ${SRV_TEMPLATE} --load-ca-certificate ca.pem --load-ca-privkey ca.key --load-privkey server.key --outfile server.pem

# Netttoyage
rm ${CA_TEMPLATE} ${SRV_TEMPLATE}

