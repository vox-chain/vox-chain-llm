
from config import load_config, get_config
from web3 import Web3
load_config()
config = get_config()
import os

w3 = Web3(Web3.HTTPProvider(config['NETWORK_URL']))
private_key = os.getenv('PK')  #config['PK']
def sign_and_send_transaction(transaction):
    account = w3.eth.account.from_key(private_key)
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    return receipt