from flask import Flask
from flask.ext.pymongo import PyMongo
from crypto import *

app = Flask(__name__)
app.config.from_object('settings')
mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/pubkey/server')
def server_pub():
    return server_key(app).exportKey()    
