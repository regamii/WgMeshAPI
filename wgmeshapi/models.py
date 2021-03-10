"""Model classes defining the database schema."""
from wgmeshapi import db


class Netaddr(db.Model):
    """Model defining the network address object."""
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), unique=False, nullable=False)
    netaddr = db.Column(db.String(18), unique=True, nullable=False)
    peers = db.relationship('Peer', backref='members', lazy='dynamic')

    def __repr__(self):
        return f"Netaddr('{self.id}', '{self.netaddr}')"


class Peer(db.Model):
    """Model defining the peers, related network addresses, object."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    netaddr_id = db.Column(db.Integer, db.ForeignKey('netaddr.id'), nullable=False)
    address = db.Column(db.String(18), unique=True, nullable=False)
    endpoint = db.Column(db.String(21), unique=True, nullable=False)
    privkey = db.Column(db.String(44), unique=True, nullable=False)

    def __repr__(self):
        return f"Peer('{self.id}', '{self.name}', '{self.netaddr_id}', '{self.address}', '{self.endpoint}', '{self.privkey}')"
