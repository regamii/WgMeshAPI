"""Model classes defining the database schema."""
from wgmeshapi import app, db
from werkzeug.security import generate_password_hash, check_password_hash
import time
import jwt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expires_in=3600):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')


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
    pubkey = db.Column(db.String(44), unique=True, nullable=False)

    def __repr__(self):
        return f"Peer('{self.id}', '{self.name}', '{self.netaddr_id}', '{self.address}', '{self.endpoint}', '{self.privkey}')"
