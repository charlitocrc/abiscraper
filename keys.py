ETHERSCAN = ''
WEBSOCKET_SERVER = 'ws://127.0.0.1:8546'
# WEBSOCKET_SERVER = 'wss://mainnet.infura.io/ws/v3/{YOUR_INFURA_KEY}'

# modify for mongodb
mongo_user = ''
mongo_password = ''
mongo_host = ''
mongo_auth_db = ''
mongo_suffix = '?tls=true&tlsAllowInvalidCertificates=true'  # optional, remove it from the one liner if not needed
mongo_one_liner = f'mongodb+srv://{mongo_user}:{mongo_password}@{mongo_host}/{mongo_auth_db}{mongo_suffix}'
