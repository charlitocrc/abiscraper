# ABIScrapper
This little tool allows to save ABI's & bytecodes from Ethereum Smart Contracts, using the Etherscan API. It saves the data on a MongoDB for later retrieval. It can be configured to save non contract addresses on the database too.


## Usage
Simply modify the keys.py file and add your own details

Websocket server address [(the free version of Infura works) ](https://infura.io/)

[Etherscan API Key](https://etherscan.io/)

MongoDB login details. [Atlas](https://www.mongodb.com/cloud/atlas/register) provides free test clusters for you to play with

Run scrap.py and you are all set. The data will be saved on 'ethereum' database within the collection 'addresses'.

Contracts will be entered on the Mongo database as they are spotted on new blocks (currently only from to/from addresses on each transaction)

![ABIScrapper demo](misc/demo.png?raw=true "Title")

## What can you do with this?
You tell me :)