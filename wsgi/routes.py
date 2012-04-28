from flask import Flask, request
from flask.ext.pymongo import PyMongo
from crypto import *

app = Flask(__name__)
app.config.from_object('settings')
mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/pubkey', methods=['POST'])
def add_pubkey():
    db = mongo.db
    username = request.form['username']
    pubkey = request.form['pubkey']
    shibboleth = request.form['shibboleth']
    signature = request.form['signature']

    key = db.keys.find_one({'username': username})
    if key:
        return '{"result": "username already exists"}', 400, {}

    if check_signature(pubkey, shibboleth, signature):
        if db.keys.insert({'username': username, 'pubkey': pubkey}):
            return '{"result": "success"}'
        return '{"result": "database failure"}', 500, {}
    return '{"result": "invalid signature"}', 400, {}

@app.route('/pubkey/server')
def server_pub():
    return server_key(app).exportKey(), 200, {'Content-Type': 'text/plain'}

@app.route('/pubkey/:username')
def get_pubkey():
    db = mongo.db
    username = request.form['username']

    entry = db.keys.find_one({'username': username})

    if entry:
        return entry['pubkey'], 200, {'Content-Type': 'text/plain'}
    else:
        return '', 404, {}

@app.route('/config')
def get_config():
    return str(dict(app.config))
