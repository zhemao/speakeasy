from Crypto.PublicKey import RSA

pubkey = RSA.importKey(open('server_public.pem').read())
