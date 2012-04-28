from Crypto.PublicKey import RSA

def server_key(app, key='PUB_KEY'):
    f = open(app.config[key], 'r')
    key = RSA.importKey(f.read())
    f.close()
    return key

