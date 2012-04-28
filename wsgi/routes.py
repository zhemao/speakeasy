from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.config.from_file('settings')
mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/filename')
def curfile():
    return __file__
