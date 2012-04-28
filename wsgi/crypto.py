from Crypto.PublicKey import RSA
from Crypto import Random

rng = Random.new().read

def check_signature(pubkey, shibboleth, signature):
    rsakey = RSA.importKey(pubkey)
    return rsakey.verify(str(shibboleth), (int(signature),))

def authenticate_user(db, app, form):
    username = form['username']
    shibboleth = form['shibboleth']
    signature = form['signature']

    key_entry = db.keys.find_one({'username': username})

    if key_entry:
        pubkey = key_entry['pubkey']
        if check_signature(pubkey, shibboleth, signature):
            serv_key = RSA.importKey(app.config['PRIV_KEY'])
            signature = serv_key.sign(str(username), rng(384))[0]
            return str(signature)
        
    return None

def current_user(app, cookies):
    username = cookies['username']
    signature = cookies['signature']

    if check_signature(app.config['PUB_KEY'], username, signature):
        return username
    return None
