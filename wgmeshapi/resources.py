"""
Classes in this file implements the flask_restful.Resource class. Near the bottom
of the file resources (defined as classes) are being added to the api variable.
"""
from wgmeshapi import app, api, db, auth
from wgmeshapi.models import User, Netaddr, Peer
from flask_restful import Resource, reqparse, abort
from flask import make_response, g
import jwt

NetaddrParser = reqparse.RequestParser()
NetaddrParser.add_argument('description', required=True, type=str,
                           help='Description to this network')
NetaddrParser.add_argument('netaddr', required=True, type=str,
                           help='Virtual network address to use')

PeersParser = reqparse.RequestParser()
PeersParser.add_argument('name', required=True, type=str, help='Name of the peer')
PeersParser.add_argument('address', required=True, type=str,
                         help='IP address in the overlay network')
PeersParser.add_argument('endpoint', required=True, type=str,
                         help='Endpoint in the \'normal\' network')
PeersParser.add_argument('pubkey', required=True, type=str,
                         help='Public key of this peer.')

UserParser = reqparse.RequestParser()
UserParser.add_argument('username', required=True, type=str,
                        help='Username is required')
UserParser.add_argument('password', required=True, type=str,
                        help='Password is required')


@auth.verify_password
def verify_password(username_or_token, password):
    try:
        data = jwt.decode(
            username_or_token.encode(),
            app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        user = User.query.get(data['id'])
    except:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


class AuthAPI(Resource):
    """Get an authentication token."""

    @auth.login_required
    def get(self):
        return {'access_token': g.user.generate_auth_token()}


class UserListAPI(Resource):
    """List and create users from/to the database context."""

    def __init__(self):
        self.admin = User.query.first()

    @auth.login_required
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

    @auth.login_required
    def post(self):
        if g.user is not self.admin:
            abort(403)

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
        except Exception:
            return {'message': 'Resource not created.'}


class UserAPI(Resource):
    """Read, update and delete users from/to the database context."""

    def __init__(self):
        self.admin = User.query.first()

    @auth.login_required
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

    @auth.login_required
    def put(self, id):
        if g.user is not self.admin and g.user is not user:
            abort(403)
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
        except Exception:
            return {'message': 'Resource not altered.'}

    @auth.login_required
    def delete(self, id):
        if g.user is not self.admin and g.user is not user:
            abort(403)
        user = User.query.get_or_404(id)

        db.session.delete(user)
        try:
            db.session.commit()
            return None, 204
        except Exception:
            return {'message': 'Resource not deleted.'}


class Token(Resource):
    """Generate JWT for a specific user."""

    def __init__(self):
        self.admin = User.query.first()

    @auth.login_required
    def get(self, id):
        user = User.query.get_or_404(id)
        if g.user is not self.admin and g.user is not user:
            abort(403)

        token = user.generate_auth_token()
        return {'access_token': token}


class NetaddrListAPI(Resource):
    """List and create network addresses from/to the database context."""

    @auth.login_required
    def get(self):
        results = Netaddr.query.all()
        netaddrs = {}
        for result in results:
            netaddrs[result.id] = {
                'description': result.description,
                'netaddr': result.netaddr
            }
        return netaddrs

    @auth.login_required
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
        except Exception:
            return {'message': 'Resource not created.'}


class NetaddrAPI(Resource):
    """Read, update and delete network addresses from/to database context."""

    @auth.login_required
    def get(self, id):
        result = Netaddr.query.get_or_404(id)
        return {
            'id': result.id,
            'description': result.description,
            'netaddr': result.netaddr
        }

    @auth.login_required
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
        except Exception:
            return {'message': 'Resource not altered.'}

    @auth.login_required
    def delete(self, id):
        netaddr = Netaddr.query.get_or_404(id)
        db.session.delete(netaddr)
        try:
            db.session.commit()
            return None, 204
        except Exception:
            return {'message': 'Resource not deleted.'}


class PeerListAPI(Resource):
    """List and create peers of/to specific network address."""

    @auth.login_required
    def get(self, id):
        results = Netaddr.query.get_or_404(id).peers
        peers = {}
        for result in results:
            peers[result.id] = {
                'name': result.name,
                'address': result.address,
                'endpoint': result.endpoint,
                'pubkey': result.pubkey
            }
        return peers

    @auth.login_required
    def post(arg, id):
        args = PeersParser.parse_args()
        netaddr = Netaddr.query.get_or_404(id)

        peer = Peer(
            name=args['name'],
            netaddr_id=netaddr.id,
            address=args['address'],
            endpoint=args['endpoint'],
            pubkey=args['pubkey']
        )
        db.session.add(peer)

        try:
            db.session.commit()
            peer = Peer.query.get(peer.id)
            return {
                'id': peer.id,
                'name': peer.name,
                'address': peer.address,
                'endpoint': peer.endpoint,
                'pubkey': peer.pubkey
            }, 201
        except Exception:
            return {'message': 'Resource not created.'}


class PeerAPI(Resource):
    """Read, update and delete peers from/to specific network address."""

    @auth.login_required
    def get(self, netaddrId, peerId):
        netaddr = Netaddr.query.get_or_404(netaddrId)
        peer = netaddr.peers.filter(Peer.id == peerId).first_or_404()
        return {
            'id': peer.id,
            'name': peer.name,
            'address': peer.address,
            'endpoint': peer.endpoint,
            'pubkey': peer.pubkey
        }

    @auth.login_required
    def put(self, netaddrId, peerId):
        args = PeersParser.parse_args()
        netaddr = Netaddr.query.get_or_404(netaddrId)
        peer = netaddr.peers.filter(Peer.id == peerId).first_or_404()

        peer.name = args['name']
        peer.address = args['address']
        peer.endpoint = args['endpoint']
        peer.pubkey = args['pubkey']
        db.session.add(peer)

        try:
            db.session.commit()
            return {
                'id': peer.id,
                'name': peer.name,
                'address': peer.address,
                'endpoint': peer.endpoint,
                'pubkey': peer.pubkey
            }
        except Exception:
            return {'message': 'Resource not altered.'}

    @auth.login_required
    def delete(self, netaddrId, peerId):
        netaddr = Netaddr.query.get_or_404(netaddrId)
        peer = netaddr.peers.filter(Peer.id == peerId).first_or_404()
        db.session.delete(peer)
        try:
            db.session.commit()
            return None, 204
        except Exception:
            return {'message': 'Resource not deleted.'}


class Config(Resource):
    """Generate WireGuard compatible configuration file."""

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

    @auth.login_required
    def get(self, netaddrId, peerId):
        netaddr = Netaddr.query.get_or_404(netaddrId)
        interface = netaddr.peers.filter(Peer.id == peerId).first_or_404()
        interface.listenPort = interface.endpoint.split(':')[1]
        peers = Peer.query.filter(Peer.id != peerId).all()

        self.config = self.config.format(
            netaddr.description,
            interface.name,
            interface.address,
            interface.listenPort
        )

        for peer in peers:
            self.config += self.peer.format(
                netaddr.description,
                peer.name,
                peer.pubkey,
                peer.address.split('/')[0] + '/32',
                peer.endpoint
            )

        response = make_response(self.config, 200)
        response.headers['content-type'] = 'text/plain'
        return response


api.add_resource(AuthAPI, '/auth')
api.add_resource(UserListAPI, '/user')
api.add_resource(UserAPI, '/user/<int:id>')
api.add_resource(Token, '/user/<int:id>/token')
api.add_resource(NetaddrListAPI, '/netaddr')
api.add_resource(NetaddrAPI, '/netaddr/<int:id>')
api.add_resource(PeerListAPI, '/netaddr/<int:id>/peer')
api.add_resource(PeerAPI, '/netaddr/<int:netaddrId>/peer/<int:peerId>')
api.add_resource(Config, '/netaddr/<int:netaddrId>/peer/<int:peerId>/config')
