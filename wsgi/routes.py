from flask import Flask, request
from flask.ext.pymongo import PyMongo
from crypto import *
from api_helpers import *
from werkzeug import secure_filename
import gridfs 

app = Flask(__name__)
app.config.from_object('settings')
mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/pubkey/add', methods=['POST'])
def add_pubkey():
    db = mongo.db
    username = request.form['username']
    pubkey = request.form['pubkey']
    shibboleth = request.form['shibboleth']
    signature = request.form['signature']

    key = db.keys.find_one({'username': username})
    if key:
        return json_error("username already exists", 400)

    if check_signature(pubkey, shibboleth, signature):
        if db.keys.insert({'username': username, 'pubkey': pubkey}):
            return json_success()
        return json_error('database insertion failure', 500)
    return json_error('invalid signature', 400)

@app.route('/pubkey/server')
def server_pub():
    return app.config['PUB_KEY'], 200, {'Content-Type': 'text/plain'}

@app.route('/pubkey/<username>')
def get_pubkey(username):
    db = mongo.db
    entry = db.keys.find_one({'username': username})

    if entry:
        return entry['pubkey'], 200, {'Content-Type': 'text/plain'}
    else:
        return '', 404, {}

   
