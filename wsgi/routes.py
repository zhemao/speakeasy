from flask import Flask, request, Response
from flask.ext.pymongo import PyMongo
from crypto import *
from api_helpers import *
from storage import *
import os

app = Flask(__name__)
app.config.from_object('settings')
mongo = PyMongo(app)

@app.route('/')
def readme():
    fname = os.getenv('OPENSHIFT_DATA_DIR') + 'README.html'
    f = open(fname)
    html = f.read()
    f.close()
    return html

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

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    signature = authenticate_user(mongo.db, app, request.form)

    resp = Response(*json_success())
    resp.set_cookie('username', username)
    resp.set_cookie('signature', signature)

    return resp

@app.route('/file/upload', methods=['POST'])
def file_upload():
    username = current_user(app, request.cookies)
    if username:    
        f = request.files['file']
        aes_key = request.headers['X-Symmetric-Key']

        if store_file(f, username, aes_key, mongo.db):
            return json_success()
        return json_error('database error', 500)

    return json_error('not authenticated', 401)
    
@app.route('/file/download/<filename>')
def file_download(filename):
    username = current_user(app, request.cookies)
    if username:
        finfo = get_fileinfo(mongo.db, username, filename)
        f = find_file(mongo.db, finfo)

        headers = {'Content-Type': f.content_type,
                   'Content-Length': f.length,
                   'Content-Disposition': 'attachment; filename='+f.filename,
                   'X-Symmetric-Key': finfo['aes_key']}

        return f.read(), 200, headers
    
    return json_error('not authenticated', 401)

@app.route('/file/list')
def file_list():
    username = current_user(app, request.cookies)
    if username:
        files = [finfo['filename'] for finfo in list_files(mongo.db, username)]
        return json_result({'result': 'success', 'files': files})
    
    return json_error('not authenticated', 401)

@app.route('/file/info/<filename>')
def file_info(filename):
    username = current_user(app, request.cookies)
    if username:
        finfo = get_fileinfo(mongo.db, username, filename)
        f = find_file(mongo.db, finfo)
        del finfo['file_id']
        del finfo['_id']
        finfo['date'] = finfo['date'].strftime('%Y-%m-%d %H:%M:%S')
        finfo['type'] = f.content_type
        finfo['length'] = f.length
        
        resp = {'result':'success', 'fileinfo':finfo}
        return json_result(resp)
    
    return json_error('not authenticated', 401)

@app.route('/file/share', methods=['POST'])
def file_share():
    username = current_user(app, request.cookies)
    if username:
        aes_key = request.headers['X-Symmetric-Key']
        recipient = request.form['recipient']
        filename = request.form['filename']
        if copy_file(mongo.db, username, recipient, filename, aes_key):
            return json_success()
    
    return json_error('not authenticated', 401)

