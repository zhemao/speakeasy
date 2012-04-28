import os

MONGO_HOST = os.getenv('OPENSHIFT_NOSQL_DB_HOST')
MONGO_PORT = os.getenv('OPENSHIFT_NOSQL_DB_PORT')
MONGO_USERNAME = os.getenv('OPENSHIFT_NOSQL_DB_USERNAME')
MONGO_PASSWORD = os.getenv('OPENSHIFT_NOSQL_DB_PASSWORD')
MONGO_DBNAME = 'speakeasy'

PRIV_KEY_FILE = os.getenv('OPENSHIFT_DATA_DIR') + '/server_private.pem'
PUB_KEY_FILE = os.getenv('OPENSHIFT_DATA_DIR') + '/server_public.pem'

PRIV_KEY = open(PRIV_KEY_FILE).read()
PUB_KEY = open(PUB_KEY_FILE).read()

DEBUG = True
