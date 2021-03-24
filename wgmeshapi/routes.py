from wgmeshapi import app, db
from wgmeshapi.models import User
from flask import render_template, redirect, url_for, abort
from flask_restful import reqparse
from wgmeshapi.resources import UserParser


@app.route('/', methods=['GET'])
def index():
    admin = User.query.first()
    if not admin:
        return render_template('register.html')
    return render_template('index.html')

@app.route('/', methods=['POST'])
def register():
    admin = User.query.first()
    if admin:
        abort(405);

    args = UserParser.parse_args()
    user = User(username=args['username'])
    user.hash_password(args['password'])
    db.session.add(user)

    try:
        db.session.commit()
        return redirect(url_for('index'))
    except Exception:
        abort(400)
