#!/bin/sh
# Entrypoint script for WgMeshAPI

# Generate secret key
sed -i "s/'secret'/$(python -c 'import os; import binascii; print(binascii.hexlify(os.urandom(32)))')/" wgmeshapi/__init__.py

# Create the SQLite database file
echo "from wgmeshapi import db\nfrom wgmeshapi.models import User, Netaddr, Peer\ndb.create_all()" | python

exec "$@"
