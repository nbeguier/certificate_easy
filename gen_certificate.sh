#!/bin/bash

SRV_CN='nicolas.bluesbox.net'
# The organization of the subject.
SRV_O='AutoSign'
# The country of the subject. Two letter code.
SRV_C='FR'
# In how many days, counting from today, this certificate will expire.
SRV_VALIDITY=364
SRV_TEMPLATE=.srv.tmp

CA_PUB_PATH='ca.pem'
CA_PRIV_PATH='ca.key'

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
ipsec_ike_key" > ${SRV_TEMPLATE}

# # Génération du certificat du serveur
certtool --generate-certificate --template ${SRV_TEMPLATE} --load-ca-certificate ${CA_PUB_PATH} \
  --load-ca-privkey ${CA_PRIV_PATH} --load-privkey server.key --outfile server.pem

# Netttoyage
rm ${SRV_TEMPLATE}

