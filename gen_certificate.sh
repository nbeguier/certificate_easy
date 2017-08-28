#!/bin/bash

SRV_CN='nicolas.bluesbox.net'
# The organization of the subject.
SRV_O='AutoSign'
# In how many days, counting from today, this certificate will expire.
SRV_VALIDITY=364

OUTPUT=$PWD

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -c|--cn)
    SRV_CN="$2"
    shift # past argument
    ;;
    -o)
    SRV_O="$2"
    shift # past argument
    ;;
    -O|--output)
    OUTPUT="$2"
    shift # past argument
    ;;
    -v|--validity)
    SRV_VALIDITY="$2"
    shift # past argument
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done

SRV_CN="${SRV_CN}"
# The organization of the subject.
SRV_O="${SRV_O}"
# The country of the subject. Two letter code.
SRV_C='FR'
# In how many days, counting from today, this certificate will expire.
SRV_VALIDITY="${SRV_VALIDITY}"
SRV_TEMPLATE=.srv.tmp

OUTPUT="${OUTPUT}"

CA_PUB_PATH="${OUTPUT}/ca.pem"
CA_PRIV_PATH="${OUTPUT}/ca.key"

# Génération de la clé privée du serveur
openssl req -x509 -newkey rsa:4096 -keyout "${OUTPUT}"/server.key -nodes -subj "/CN=${SRV_CN}/O=${SRV_O}/C=${SRV_C}"

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
  --load-ca-privkey ${CA_PRIV_PATH} --load-privkey "${OUTPUT}"/server.key --outfile "${OUTPUT}"/server.pem

# Netttoyage
rm ${SRV_TEMPLATE}
