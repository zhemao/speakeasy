from flask import Flask
from flask.ext import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/filename')
def curfile():
    return __file__
