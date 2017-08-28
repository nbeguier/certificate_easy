#!/bin/bash

CA_CN='TestCA'
# The organization of the subject.
CA_O='AutoSign'
CA_VALIDITY=365
OUTPUT=$PWD

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -c|--cn)
    CA_CN="$2"
    shift # past argument
    ;;
    -o)
    CA_O="$2"
    shift # past argument
    ;;
    -O|--output)
    OUTPUT="$2"
    shift # past argument
    ;;
    -v|--validity)
    CA_VALIDITY="$2"
    shift # past argument
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done

CA_CN="${CA_CN}"
# The organization of the subject.
CA_O="${CA_O}"
# The country of the subject. Two letter code.
CA_C='FR'
# In how many days, counting from today, this certificate will expire.
CA_VALIDITY="${CA_VALIDITY}"
CA_TEMPLATE=.ca.tmp
OUTPUT="${OUTPUT}"

# Génération de la clé privée de la CA
openssl req -x509 -newkey rsa:4096 -keyout "${OUTPUT}"/ca.key -nodes -subj "/CN=${CA_CN}/O=${CA_O}/C=${CA_C}"

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
certtool --generate-self-signed --load-privkey "${OUTPUT}"/ca.key --template ${CA_TEMPLATE} --outfile "${OUTPUT}"/ca.pem

rm ${CA_TEMPLATE}