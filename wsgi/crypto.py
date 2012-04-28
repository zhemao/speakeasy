from Crypto.PublicKey import RSA

def server_key(app, key='PUB_KEY'):
    f = open(app.config[key], 'r')
    key = RSA.importKey(f.read())
    f.close()
    return key

def check_signature(pubkey, shibboleth, signature):
    try:
        rsakey = RSA.importKey(pubkey)
        return rsakey.verify(shibboleth, (int(signature),))
    except ValueError:
        return False
