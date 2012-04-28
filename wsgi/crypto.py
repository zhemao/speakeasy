from Crypto.PublicKey import RSA

def check_signature(pubkey, shibboleth, signature):
    rsakey = RSA.importKey(pubkey)
    return rsakey.verify(str(shibboleth), (int(signature),))

def current_user(app, cookies):
    username = cookies['username']
    signature = cookies['signature']

    if check_signature(app['PUB_KEY'], username, signature):
        return username
    return None
