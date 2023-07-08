# Setup
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

url_test_polygon = "https://rpc.ankr.com/polygon_mumbai"
contract_address = "0x54EEDe47850fE932f5466B6fa708bf1176371966"
contract_abi = json.loads(
    '''[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"collection","type":"address"},{"indexed":false,"internalType":"string","name":"name","type":"string"},{"indexed":false,"internalType":"string","name":"symbol","type":"string"}],"name":"CollectionCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"collection","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"string","name":"tokenURI","type":"string"}],"name":"TokenMinted","type":"event"},{"inputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"string","name":"baseURI","type":"string"}],"name":"deployCollection","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract Collection","name":"collection","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]''')
account_1_addresses = '0xDF0D85Ba488cFBc36dd9e68ba956999a42F15879'
account_1_private_key = 'ebc9c7c1536422bd042cbacf4384e78fe335e6fd67c5a2dfc33658257c363a53'

client_web3 = Web3(Web3.HTTPProvider(url_test_polygon))
client_web3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(client_web3.is_connected())

contract = client_web3.eth.contract(contract_address, abi=contract_abi)

# parameters for deployCollection
name = 'tester'
symbol = 'TST'
baseURI = 'test.io'

nonce = client_web3.eth.get_transaction_count(account_1_addresses)


transaction_params = {
    'from': account_1_addresses,
    'gas': 2000005,  # Укажите желаемый лимит газа (gas limit)
    'gasPrice': client_web3.to_wei(2, 'gwei'),  # Укажите желаемую цену газа (gas price) в гвей,
    'nonce': nonce
}

transaction = contract.functions.deployCollection(name, symbol, baseURI).build_transaction(transaction_params)

signed_transaction = client_web3.eth.account.sign_transaction(transaction, private_key=account_1_private_key)

transaction_hash = client_web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

transaction_receipt = client_web3.eth.wait_for_transaction_receipt(transaction_hash)

get_transaction_receipt = client_web3.eth.get_transaction_receipt(transaction_hash)
if transaction_receipt['status'] == 0x0:
    print("Транзакция не выполнена успешно")
    gas_used = transaction_receipt['gasUsed']
    print("Количество использованного газа:", gas_used)

