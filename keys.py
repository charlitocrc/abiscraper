
# todo add mysql sqlite files handling

# WEBSOCKET_SERVER = 'wss://mainnet.infura.io/ws/v3/{YOUR_INFURA_KEY}'
WEBSOCKET_SERVER = ''
ETHERSCAN = ''

# modify for mongodb
mongo_user = ''
mongo_password = ''
mongo_host = ''
mongo_auth_db = ''
mongo_suffix = '?tls=true&tlsAllowInvalidCertificates=true'  # optional, remove it from the one liner if not needed
mongo_one_liner = f'mongodb+srv://{mongo_user}:{mongo_password}@{mongo_host}/{mongo_auth_db}{mongo_suffix}'
