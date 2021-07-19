"""This file holds all Request Parsers"""
from flask_restful import reqparse

NetaddrParser = reqparse.RequestParser()
NetaddrParser.add_argument('description', required=True, type=str,
                           help='Description to this network')
NetaddrParser.add_argument('netaddr', required=True, type=str,
                           help='Virtual network address to use')

PeerParser = reqparse.RequestParser()
PeerParser.add_argument('friendlyname', required=True, type=str, help='Name of the peer')
PeerParser.add_argument('address', required=True, type=str,
                         help='IP address in the overlay network')
PeerParser.add_argument('endpoint', required=True, type=str,
                         help='Endpoint in the \'normal\' network')
PeerParser.add_argument('pubkey', required=True, type=str,
                         help='Public key of this peer.')

UserParser = reqparse.RequestParser()
UserParser.add_argument('username', required=True, type=str,
                        help='Username is required')
UserParser.add_argument('password', required=True, type=str,
                        help='Password is required')
