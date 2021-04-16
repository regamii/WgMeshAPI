from wgmeshapi import app, db
from wgmeshapi.models import User
from wgmeshapi.parsers import UserParser
from flask import render_template, redirect, url_for, abort


@app.route('/', methods=['GET'])
def index():
    admin = User.query.first()
    if not admin:
        return render_template('register.html', title='Register Admin')
    return render_template('index.html', title='Documentation')


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
        return redirect(url_for('index'))
    except:
        abort(400)

@app.route('/token')
def token():
    return render_template('token.html', title='Token')

@app.route('/user/get')
def user_get():
    return render_template('user/get.html', title='User Get')

@app.route('/user/post')
def user_post():
    return render_template('user/post.html', title='User Get')

@app.route('/user/id/delete')
def user_id_delete():
    return render_template('user/id/delete.html', title='User Id Delete')

@app.route('/user/id/get')
def user_id_get():
    return render_template('user/id/get.html', title='User Id Get')

@app.route('/user/id/put')
def user_id_put():
    return render_template('user/id/put.html', title='User Id Put')

@app.route('/netaddr/get')
def netaddr_get():
    return render_template('netaddr/get.html', title='Netaddr Get')

@app.route('/netaddr/post')
def netaddr_post():
    return render_template('netaddr/post.html', title='Netaddr Post')

@app.route('/netaddr/id/delete')
def netaddr_id_delete():
    return render_template('netaddr/id/delete.html', title='Netaddr Id Delete')

@app.route('/netaddr/id/get')
def netaddr_id_get():
    return render_template('netaddr/id/get.html', title='Netaddr Id Get')

@app.route('/netaddr/id/put')
def netaddr_id_put():
    return render_template('netaddr/id/put.html', title='Netaddr Id Put')

@app.route('/peer/get')
def peer_get():
    return render_template('peer/get.html', title='Peer Get')

@app.route('/peer/post')
def peer_post():
    return render_template('peer/post.html', title='Peer Post')

@app.route('/peer/id/delete')
def peer_id_delete():
    return render_template('peer/id/delete.html', title='Peer Delete')

@app.route('/peer/id/get')
def peer_id_get():
    return render_template('peer/id/get.html', title='Peer Get')

@app.route('/peer/id/put')
def peer_id_put():
    return render_template('peer/id/put.html', title='Peer Put')

@app.route('/peer/id/config')
def peer_id_config():
    return render_template('peer/id/config.html', title='Peer Config')
