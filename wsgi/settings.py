import os

MONGO_HOST = os.getenv('OPENSHIFT_NOSQL_DB_HOST')
MONGO_PORT = os.getenv('OPENSHIFT_NOSQL_DB_PORT')
MONGO_USERNAME = os.getenv('OPENSHIFT_NOSQL_DB_USERNAME')
MONGO_PASSWORD = os.getenv('OPENSHIFT_NOSQL_DB_PASSWORD')