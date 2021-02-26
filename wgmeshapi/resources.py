from wgmeshapi import api, db
from wgmeshapi.models import Netaddr
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('description', required=True, type=str, help='Description to this network')
parser.add_argument('netaddr', required=True, type=str, help='Virtual network address to use')


class NetworkAddressList(Resource):
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
        args = parser.parse_args()
        netaddr = Netaddr(description=args['description'], netaddr=args['netaddr'])
        db.session.add(netaddr)
        try:
            db.session.commit()
        except Exception:
            return {'message': 'Resource not created.'}
        return {'message': 'Resource created.'}, 201


class NetworkAddress(Resource):
    def get(self, id):
        result = Netaddr.query.get_or_404(id)
        return {
            'id': result.id,
            'description': result.description,
            'netaddr': result.netaddr
            }

    def put(self, id):
        args = parser.parse_args()
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

    def delete(self, id):
        netaddr = Netaddr.query.get_or_404(id)
        db.session.delete(netaddr)
        try:
            db.session.commit()
            return None, 204
        except Exception:
            return {'message': 'Resource not deleted.'}

api.add_resource(NetworkAddressList, '/netaddr')
api.add_resource(NetworkAddress, '/netaddr/<int:id>')
