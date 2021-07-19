from wgmeshapi import app, db
from wgmeshapi.models import User
from wgmeshapi.parsers import UserParser
from flask import render_template, redirect, url_for, abort


@app.route('/', methods=['GET'])
def index():
    admin = User.query.first()
    if not admin:
        return render_template('register.html', title='Register Admin')
    return redirect('/api/token')


@app.route('/', methods=['POST'])
def register():
    admin = User.query.first()
    if admin:
        abort(405)

    args = UserParser.parse_args()
    user = User(username=args['username'])
    user.hash_password(args['password'])
    db.session.add(user)

    try:
        db.session.commit()
        return redirect('/api/token')
    except:
        abort(400)
