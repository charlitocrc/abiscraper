
# todo add mysql sqlite files handling

# WEBSOCKET_SERVER = 'wss://mainnet.infura.io/ws/v3/YOUR_INFURA_KEY'
WEBSOCKET_SERVER = ''
ETHERSCAN = ''
DATA_SAVING_METHOD = 'mongo'  # accepted_values: files, mongo, sqlite3, mysql


# modify for mongodb
mongo_user = ''
mongo_password = ''
mongo_host = ''
mongo_auth_db = ''
mongo_suffix = ''  # optional
mongo_one_liner = f'mongodb+srv://{mongo_user}:{mongo_password}@{mongo_host}/{mongo_auth_db}{mongo_suffix}'


# todo: possibly not needed
db_dict = {
    "mongo": {
        "user": "X",
        "password": "X",
        "host": "x",
        "database": "x",
        "port": 0,
        "one_liner": "x"
    },
    "sqlite": {
        "filename": "x"
    },
    "mysql": {
        "user": "X",
        "password": "X",
        "host": "x",
        "database": "x",
        "port": 0,
    }

}
