import KeyGen

user_db = {}
for _ in range(6):
    priv_key, pub_key = KeyGen.generateKeyPair()
    user_db[pub_key.to_string().hex()] = {"priv_key": priv_key, "balance": 100}