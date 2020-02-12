from .crypto import clsSysEncrypt, clsSysDecrypt

def sys_crypto_routes(api):
    api.add_resource(clsSysEncrypt, '/api/v1/encrypt')
    api.add_resource(clsSysDecrypt, '/api/v1/decrypt')