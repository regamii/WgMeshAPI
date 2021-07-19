"""
Classes in this file implements the flask_restful.Resource class. Near the bottom
of the file resources (defined as classes) are being added to the api variable.
"""
from wgmeshapi import app, api_bp, api, db, auth
from wgmeshapi.models import User, Netaddr, Peer
from wgmeshapi.parsers import UserParser, NetaddrParser, PeerParser
from flask_restful import Resource, abort
from flask import g, request, make_response
from functools import wraps
import jwt


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.client = user
    return True

def jwt_decode():
    token = None
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
    if not token:
        return
    try:
        data = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
    except:
        return
    return data

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data = jwt_decode()
        if not data:
            return {'message': 'Token is invalid'}, 401
        elif 'pubkey' in data:
            return {'message': 'Unauthorized'}, 401
        g.user = User.query.get(data['id'])
        return f(*args, **kwargs)
    return wrapper

def peer_token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data = jwt_decode()
        if not data:
            return {'message': 'Peer token required'}, 401
        elif 'id' in data:
            return {'message': 'Token is invalid'}, 401
        g.peer = Peer.query.filter_by(pubkey=data['pubkey']).first()
        return f(*args, **kwargs)
    return wrapper


class Token(Resource):
    """Generate JWT for a specific user."""

    @auth.login_required
    def get(self):
        return {'access_token': g.client.generate_auth_token()}


class UserAPI(Resource):
    """Read, update and delete user from/to the database context."""
    method_decorators = [token_required]

    def __init__(self):
        self.user = User.query.first()

    def get(self):
        return {
            'id': self.user.id,
            'username': self.user.username,
        }

    def put(self):
        args = UserParser.parse_args()
        self.user.username = args['username']
        self.user.hash_password(args['password'])
        db.session.add(self.user)

        try:
            db.session.commit()
            return {
                'id': self.user.id,
                'username': self.user.username
            }
        except:
            return {'message': 'The action could not be successfully performed. This could be due to unique constraints in the database, or the database not being available.'}, 500

    def delete(self):
        db.session.delete(self.user)
        try:
            db.session.commit()
            return None, 204
        except:
            return {'message': 'The action could not be successfully performed. This could be due to unique constraints in the database, or the database not being available.'}, 500


class NetaddrListAPI(Resource):
    """List and create network addresses from/to the database context."""
    method_decorators = [token_required]

    def get(self):
        results = Netaddr.query.all()
        netaddrs = {}
        for result in results:
            netaddrs[result.id] = {
                'description': result.description,
                'netaddr': result.netaddr
            }
        return netaddrs

    def post(self):
        args = NetaddrParser.parse_args()
        netaddr = Netaddr(
            description=args['description'],
            netaddr=args['netaddr']
        )
        db.session.add(netaddr)

        try:
            db.session.commit()
            return {
                'id': netaddr.id,
                'description': netaddr.description,
                'netaddr': netaddr.netaddr
            }, 201
        except:
            return {'message': 'The action could not be successfully performed. This could be due to unique constraints in the database, or the database not being available.'}, 500


class NetaddrAPI(Resource):
    """Read, update and delete network addresses from/to database context."""
    method_decorators = [token_required]

    def get(self, id):
        result = Netaddr.query.get_or_404(id)
        return {
            'id': result.id,
            'description': result.description,
            'netaddr': result.netaddr
        }

    def put(self, id):
        args = NetaddrParser.parse_args()
        netaddr = Netaddr.query.get_or_404(id)

        netaddr.description = args['description']
        netaddr.netaddr = args['netaddr']
        db.session.add(netaddr)

        try:
            db.session.commit()
            return {
                'id': netaddr.id,
                'description': netaddr.description,
                'netaddr': netaddr.netaddr
            }
        except:
            return {'message': 'The action could not be successfully performed. This could be due to unique constraints in the database, or the database not being available.'}, 500

    def delete(self, id):
        netaddr = Netaddr.query.get_or_404(id)
        db.session.delete(netaddr)
        try:
            db.session.commit()
            return None, 204
        except:
            return {'message': 'The action could not be successfully performed. This could be due to unique constraints in the database, or the database not being available.'}, 500


class PeerListAPI(Resource):
    """List and create peers of/to specific network address."""
    method_decorators = [token_required]

    def get(self, id):
        results = Netaddr.query.get_or_404(id).peers
        peers = {}
        for result in results:
            peers[result.id] = {
                'friendlyname': result.friendlyname,
                'address': result.address,
                'endpoint': result.endpoint,
                'pubkey': result.pubkey,
                'access_token': result.apikey
            }
        return peers

    def post(arg, id):
        args = PeerParser.parse_args()
        netaddr = Netaddr.query.get_or_404(id)

        peer = Peer(
            netaddr_id=netaddr.id,
            friendlyname=args['friendlyname'],
            address=args['address'],
            endpoint=args['endpoint'],
            pubkey=args['pubkey'],
            apikey=jwt.encode(
                {'pubkey': args['pubkey']},
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        )
        db.session.add(peer)

        try:
            db.session.commit()
            return {
                'friendlyname': peer.friendlyname,
                'address': peer.address,
                'endpoint': peer.endpoint,
                'pubkey': peer.pubkey,
                'access_token': peer.apikey
            }, 201
        except:
            return {'message': 'The action could not be successfully performed. This could be due to unique constraints in the database, or the database not being available.'}, 500


class PeerAPI(Resource):
    """Read, update and delete peers from/to specific network address."""
    method_decorators = [token_required]

    def get(self, netaddrId, peerId):
        netaddr = Netaddr.query.get_or_404(netaddrId)
        peer = netaddr.peers.filter(Peer.id == peerId).first_or_404()
        return {
            'id': peer.id,
            'friendlyname': peer.friendlyname,
            'address': peer.address,
            'endpoint': peer.endpoint,
            'pubkey': peer.pubkey,
            'access_token': peer.apikey
        }

    def put(self, netaddrId, peerId):
        args = PeerParser.parse_args()
        netaddr = Netaddr.query.get_or_404(netaddrId)
        peer = netaddr.peers.filter(Peer.id == peerId).first_or_404()

        peer.friendlyname = args['friendlyname']
        peer.address = args['address']
        peer.endpoint = args['endpoint']
        peer.pubkey = args['pubkey']
        peer.apikey = jwt.encode(
            {'pubkey': args['pubkey']},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        db.session.add(peer)

        try:
            db.session.commit()
            return {
                'id': peer.id,
                'friendlyname': peer.friendlyname,
                'address': peer.address,
                'endpoint': peer.endpoint,
                'pubkey': peer.pubkey,
                'access_token': peer.apikey
            }
        except:
            return {'message': 'The action could not be successfully performed. This could be due to unique constraints in the database, or the database not being available.'}, 500

    def delete(self, netaddrId, peerId):
        netaddr = Netaddr.query.get_or_404(netaddrId)
        peer = netaddr.peers.filter(Peer.id == peerId).first_or_404()
        db.session.delete(peer)
        try:
            db.session.commit()
            return None, 204
        except:
            return {'message': 'The action could not be successfully performed. This could be due to unique constraints in the database, or the database not being available.'}, 500


class Config(Resource):
    """Generate WireGuard compatible configuration file."""
    method_decorators = [peer_token_required]

    def __init__(self):
        self.config = """[Interface]
# Network: {}
# Name: {}
Address = {}
ListenPort = {}
PrivateKey = PLACEHOLDER\n\n"""
        self.peer = """[Peer]
# Network: {}
# Name: {}
PublicKey = {}
AllowedIPs = {}
Endpoint = {}\n\n"""

    def get(self):
        peers = Peer.query.filter(Peer.id != g.peer.id).all()
        self.config = self.config.format(
            g.peer.members.description,
            g.peer.friendlyname,
            g.peer.address,
            g.peer.endpoint.split(':')[1]
        )

        for peer in peers:
            self.config += self.peer.format(
                peer.members.description,
                peer.friendlyname,
                peer.pubkey,
                peer.address.split('/')[0] + '/32',
                peer.endpoint
            )

        response = make_response(self.config, 200)
        response.headers['content-type'] = 'text/plain'
        return response


api.add_resource(Token, '/token')
api.add_resource(UserAPI, '/user')
api.add_resource(NetaddrListAPI, '/netaddr')
api.add_resource(NetaddrAPI, '/netaddr/<int:id>')
api.add_resource(PeerListAPI, '/netaddr/<int:id>/peer')
api.add_resource(PeerAPI, '/netaddr/<int:netaddrId>/peer/<int:peerId>')
api.add_resource(Config, '/config')
app.register_blueprint(api_bp, url_prefix='/api')
