#!/bin/bash

if [ ! -d $HOME/.pki/nssdb ]; then

    mkdir -p $HOME/.pki/nssdb
    certutil -N -d sql:$HOME/.pki/nssdb --empty-password
else
    echo "Database already exists."
fi

CERT_FILE="/root/.mitmproxy/mitmproxy-ca.pem"


if [ -f "$CERT_FILE" ]; then
    certutil -d sql:$HOME/.pki/nssdb -A -t "C,," -n mitmproxy -i /root/.mitmproxy/mitmproxy-ca.pem
    #sudo cp /root/.mitmproxy/mitmproxy-ca-cert.pem /etc/ssl/certs/mitmproxy-ca-cert.pem
    echo "Certificate added successfully."
else
    echo "Certificate not found."
fi

