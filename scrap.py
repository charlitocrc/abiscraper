# todo
#   add docs on functions
#   add exception handling
#   add better logging
#   add checking of identical contract codes, to make less queries to etherscan

import json
import requests
import asyncio
import time
from hexbytes import HexBytes
from web3 import Web3, exceptions
import keys
import logging
from motor.motor_asyncio import (
    AsyncIOMotorClient as MotorClient,
)
logging.basicConfig(filename=f'scrapper.log', format='%(levelname)s:%(message)s\n\n', level=logging.WARNING)

w3_obj = Web3(Web3.WebsocketProvider(keys.WEBSOCKET_SERVER))  # init web3py websocket client

# init MongoDB database cursor
client = MotorClient(keys.mongo_one_liner)
client.get_io_loop = asyncio.get_running_loop
cursor = client.ethereum

addresses_bowl = []  # stores addresses in mem to avoid unnecessary calls


def get_abi(address):
    """
    gets the abi from etherscan
    :param address: ethereum addressto retrieve abi from
    :return: 0 if error, str(abi) if abi found
    """
    url = f'https://api.etherscan.io/api?apiKey={keys.ETHERSCAN}&module=contract&action=getabi&address={address}'
    try:
        data = requests.get(url, timeout=(5, 10))
    except requests.exceptions.Timeout:
        # wait 5 more seconds and retry
        print(f'Address {address} timeout, retrying in 5s')
        time.sleep(5)
        data = requests.get(url, timeout=(5, 10))

    except requests.exceptions.RequestException as e:
        logging.exception(f'Request to {address} on Etherscan error: {e}. Returning None')
        return 0

    try:
        abi = json.loads(data.text)
        if abi['status'] == "0":
            return 0
        else:
            return abi['result']
    except Exception:
        # catchall
        return 0


async def get_stored_addresses():
    """
    creates a global list with the addresses
    this list will allow the script to check in memory if we have already checked a specific address
    :return:
    """
    global addresses_bowl
    print('Loading public keys')
    addresses_bowl.clear()  # empty the list
    start = time.time()
    doc = cursor['addresses'].find({}, {"_id": 0, "p": 1})
    async for document in doc:
        addresses_bowl.append(document['p'])

    print(f'Loaded public keys in {time.time()-start}')


def prepare_document(address, address_type, abi, code):
    """

    :param address: str() ethereum public key
    :param address_type: int() 1 if contract, 0 if 'normal address'
    :param abi: str() of ABI if contract
    :param code: bytescode of contract if available
    :return: dict() to be inserted in the database
    """
    document = {"p": address,
                "a": abi,
                "c": code,
                "s": address_type,
                # "l": None,  # label, optional
                "t": int(time.time()),  # the current time
                }
    return document


async def handler(event):
    """
    handles each block data
    :param event: new block data
    :return: None
    """
    block_hash = HexBytes.hex(event)

    # lets get all transactions
    try:
        block_data = w3_obj.eth.getBlock(block_hash, full_transactions=True)
    except exceptions.BlockNotFound:
        time.sleep(5)
        block_data = w3_obj.eth.getBlock(block_hash, full_transactions=True)

    print(f"New block: #{block_data['number']}")
    txn_list = block_data['transactions']
    x = 0
    operations = []
    for txn in txn_list:
        try:
            x += 1
            from_address = txn['from']
            if from_address not in addresses_bowl:
                addresses_bowl.append(from_address)  # add address to bowl
                from_bytecode = w3_obj.eth.get_code(from_address)  # get bytecode
                if from_bytecode == b'':
                    # this is a normal account, just insert
                    # dont check for abi
                    operations.append(prepare_document(from_address, 0, None, None))
                else:
                    from_abi = get_abi(from_address)
                    operations.append(prepare_document(from_address, 1, from_abi, from_bytecode))

            to_address = txn['to']
            if to_address not in addresses_bowl:
                addresses_bowl.append(to_address)  # add address to bowl
                from_bytecode = w3_obj.eth.get_code(to_address)  # get bytecode
                if from_bytecode == b'':
                    # this is a normal account, just insert
                    # dont check for abi
                    operations.append(prepare_document(to_address, 0, None, None))
                else:
                    from_abi = get_abi(to_address)
                    operations.append(prepare_document(to_address, 1, from_abi, from_bytecode))
        except Exception as e:
            logging.exception(e, block_hash)
        print(f"Processed txn {x} from block #{block_data['number']}")

    # insert all data
    if operations:
        # if the operations dict is not empty, attempt insert
        await cursor['addresses'].insert_many(operations)

    print(f"Finished processing block #{block_data['number']}")


async def log_loop(event_filter, poll_interval):
    """
    loops on the eth filter
    :param event_filter: 'latest' blocks
    :param poll_interval: how often to query for blocks
    :return: None
    """
    await get_stored_addresses()

    while True:
        for block in event_filter.get_new_entries():
            await handler(block)  # process this blocks data
        await asyncio.sleep(poll_interval)  # wait a bit before checking again


def main():
    block_filter = w3_obj.eth.filter('latest')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(log_loop(block_filter, 2)))

# asyncio.run(get_stored_addresses())


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as err:
            logging.exception(err, 'MAINTHREAD ERROR')
