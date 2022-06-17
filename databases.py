import asyncio
import keys
from motor.motor_asyncio import (
    AsyncIOMotorClient as MotorClient,
)


def init_mongo():
    # todo add documentation
    client = MotorClient(keys.mongo_one_liner)
    client.get_io_loop = asyncio.get_running_loop
    cursor = client.ethereum
    return cursor


def init_cursor(_method):
    # todo
    #   add proper exception handling
    #   init sqlite
    #   init files
    #   init mysql
    """
    inits the cursor for database
    :return: str() if errors, else cursor object()
    """
    accepted_methods = ['files', 'mongo', 'sqlite', 'mysql']

    if _method not in accepted_methods:
        return 'MethodError'

    elif _method == 'files':
        return None

    elif _method == 'mongo':
        # init motor
        return init_mongo()

    elif _method == 'sqlite':
        # init sqlite database
        return True

    elif _method == 'mysql':
        # init pymysql cursor
        return True

    else:
        return None
