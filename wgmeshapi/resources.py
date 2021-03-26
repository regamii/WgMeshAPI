"""
Classes in this file implements the flask_restful.Resource class. Near the bottom
of the file resources (defined as classes) are being added to the api variable.
"""
from wgmeshapi import app, api, db, auth
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
    g.user = user
    return True

def token_required_for(type_of_user):
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                return {'message': 'Token is missing'}, 401

            try:
                data = jwt.decode(
                    token.encode(),
                    app.config['SECRET_KEY'],
                    algorithms=['HS256']
                )
                user = User.query.get(data['id'])
                g.user = user

                if type_of_user == 'user' and user.peer is not None:
                    return abort(401)

            except:
                return {'message': 'Token is invalid'}, 401
            return f(*args, **kwargs)
        return decorated
    return token_required


class Token(Resource):
    """Generate JWT for a specific user."""

    @auth.login_required
    def get(self):
        return {'access_token': g.user.generate_auth_token()}


class UserListAPI(Resource):
    """List and create users from/to the database context."""
    method_decorators = {token_required_for('user')}

    def __init__(self):
        self.admin = User.query.first()

    def get(self):
        results = User.query.all()
        users = {}
        for result in results:
            if result is self.admin:
                users[result.id] = {
                    'username': result.username,
                    'admin': True
                }
            else:
                users[result.id] = {
                    'username': result.username,
                    'admin': False
                }
        return users

    def post(self):
        if g.user is not self.admin:
            abort(401)

        args = UserParser.parse_args()
        user = User(username=args['username'])
        user.hash_password(args['password'])
        db.session.add(user)

        try:
            db.session.commit()
            return {
                'id': user.id,
                'username': user.username,
                'admin': False
            }, 201
        except:
            return {'message': 'Resource not created.'}


class UserAPI(Resource):
    """Read, update and delete users from/to the database context."""
    method_decorators = {token_required_for('user')}

    def __init__(self):
        self.admin = User.query.first()

    def get(self, id):
        result = User.query.get_or_404(id)

        if result is self.admin:
            return {
                'id': result.id,
                'username': result.username,
                'admin': True
            }

        return {
            'id': result.id,
            'username': result.username,
            'admin': False
        }

    def put(self, id):
        if g.user is not self.admin and g.user is not user:
            abort(401)
        user = User.query.get_or_404(id)

        args = UserParser.parse_args()
        user.username = args['username']
        user.hash_password(args['password'])
        db.session.add(user)

        try:
            db.session.commit()
            if user is self.admin:
                return {
                    'id': user.id,
                    'username': user.username,
                    'admin': True
                }

            return {
                'id': user.id,
                'username': user.username,
                'admin': False
            }
        except:
            return {'message': 'Resource not altered.'}

    def delete(self, id):
        if g.user is not self.admin and g.user is not user:
            abort(401)
        user = User.query.get_or_404(id)

        db.session.delete(user)
        try:
            db.session.commit()
            return None, 204
        except:
            return {'message': 'Resource not deleted.'}


class NetaddrListAPI(Resource):
    """List and create network addresses from/to the database context."""
    method_decorators = {token_required_for('user')}

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
            return {'message': 'Resource not created.'}


class NetaddrAPI(Resource):
    """Read, update and delete network addresses from/to database context."""
    method_decorators = {token_required_for('user')}

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
            return {'message': 'Resource not altered.'}

    def delete(self, id):
        netaddr = Netaddr.query.get_or_404(id)
        db.session.delete(netaddr)
        try:
            db.session.commit()
            return None, 204
        except:
            return {'message': 'Resource not deleted.'}


class PeerListAPI(Resource):
    """List and create peers of/to specific network address."""
    method_decorators = {token_required_for('user')}

    def get(self, id):
        results = Netaddr.query.get_or_404(id).peers
        peers = {}
        for result in results:
            peers[result.id] = {
                'user_id': result.user.id,
                'name': result.user.username,
                'address': result.address,
                'endpoint': result.endpoint,
                'pubkey': result.pubkey
            }
        return peers

    def post(arg, id):
        args = PeerParser.parse_args()
        netaddr = Netaddr.query.get_or_404(id)

        try:
            user = User(username=args['name'])
            user.hash_password(args['password'])
            db.session.add(user)
            db.session.commit()

            peer = Peer(
                netaddr_id=netaddr.id,
                user_id=user.id,
                address=args['address'],
                endpoint=args['endpoint'],
                pubkey=args['pubkey']
            )
            db.session.add(peer)
            db.session.commit()

            return {
                'id': peer.id,
                'user_id': peer.user.id,
                'name': peer.user.username,
                'address': peer.address,
                'endpoint': peer.endpoint,
                'pubkey': peer.pubkey
            }, 201
        except:
            return {'message': 'Resource not created.'}


class PeerAPI(Resource):
    """Read, update and delete peers from/to specific network address."""
    method_decorators = {token_required_for('user')}

    def get(self, netaddrId, peerId):
        netaddr = Netaddr.query.get_or_404(netaddrId)
        peer = netaddr.peers.filter(Peer.id == peerId).first_or_404()
        return {
            'id': peer.id,
            'user_id': peer.user.id,
            'name': peer.user.username,
            'address': peer.address,
            'endpoint': peer.endpoint,
            'pubkey': peer.pubkey
        }

    def put(self, netaddrId, peerId):
        args = PeerParser.parse_args()
        netaddr = Netaddr.query.get_or_404(netaddrId)
        peer = netaddr.peers.filter(Peer.id == peerId).first_or_404()

        peer.user.username = args['name']
        peer.address = args['address']
        peer.endpoint = args['endpoint']
        peer.pubkey = args['pubkey']
        db.session.add(peer)

        try:
            db.session.commit()
            return {
                'id': peer.id,
                'user_id': peer.user.id,
                'name': peer.user.username,
                'address': peer.address,
                'endpoint': peer.endpoint,
                'pubkey': peer.pubkey
            }
        except:
            return {'message': 'Resource not altered.'}

    def delete(self, netaddrId, peerId):
        netaddr = Netaddr.query.get_or_404(netaddrId)
        peer = netaddr.peers.filter(Peer.id == peerId).first_or_404()
        user = peer.user
        db.session.delete(peer)
        db.session.delete(user)
        try:
            db.session.commit()
            return None, 204
        except:
            return {'message': 'Resource not deleted.'}


class Config(Resource):
    """Generate WireGuard compatible configuration file."""
    method_decorators = {token_required_for('peer')}

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

    def get(self, netaddrId, peerId):
        netaddr = Netaddr.query.get_or_404(netaddrId)
        interface = netaddr.peers.filter(Peer.id == peerId).first_or_404()
        interface.listenPort = interface.endpoint.split(':')[1]
        peers = Peer.query.filter(Peer.id != peerId).all()

        self.config = self.config.format(
            netaddr.description,
            interface.user.username,
            interface.address,
            interface.listenPort
        )

        for peer in peers:
            self.config += self.peer.format(
                netaddr.description,
                peer.user.username,
                peer.pubkey,
                peer.address.split('/')[0] + '/32',
                peer.endpoint
            )

        response = make_response(self.config, 200)
        response.headers['content-type'] = 'text/plain'
        return response


api.add_resource(Token, '/token')
api.add_resource(UserListAPI, '/user')
api.add_resource(UserAPI, '/user/<int:id>')
api.add_resource(NetaddrListAPI, '/netaddr')
api.add_resource(NetaddrAPI, '/netaddr/<int:id>')
api.add_resource(PeerListAPI, '/netaddr/<int:id>/peer')
api.add_resource(PeerAPI, '/netaddr/<int:netaddrId>/peer/<int:peerId>')
api.add_resource(Config, '/netaddr/<int:netaddrId>/peer/<int:peerId>/config')
