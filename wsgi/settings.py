import os

MONGO_HOST = os.getenv('OPENSHIFT_NOSQL_DB_HOST')
MONGO_PORT = os.getenv('OPENSHIFT_NOSQL_DB_PORT')
MONGO_USERNAME = os.getenv('OPENSHIFT_NOSQL_DB_USERNAME')
MONGO_PASSWORD = os.getenv('OPENSHIFT_NOSQL_DB_PASSWORD')

PRIV_KEY = os.getenv('OPENSHIFT_DATA_DIR') + '/server_private.pem'
PUB_KEY = os.getenv('OPENSHIFT_DATA_DIR') + '/server_public.pem'

DEBUG = True
