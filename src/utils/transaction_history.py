import json
import requests
from config import load_config, get_config

headers = {'Content-Type': 'application/json'}
load_config()
config = get_config()

def get_latest_Block_number():

    rpc_call = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    response = requests.post(config['NETWORK_URL'], headers=headers, data= json.dumps(rpc_call))
    if response.status_code ==200:
        return int(response.json()['result'], 16)
    else:
        print('Failed to get the latest block number', response.text)
        return None



def get_block_by_number(block_number):
    rpc_call = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],
        "id": 1
    }
    response = requests.post(config['NETWORK_URL'], headers=headers, data=json.dumps(rpc_call))
    if response.status_code == 200:
        return response.json()['result']
    else:
        print(f"Failed to fetch block {block_number} ", response.text)


def find_transactions_by_account(account, start_block, end_block):
    account = account.lower()
    transactions = []


    for block_number in range(start_block, end_block):
        block =get_block_by_number(block_number)
        if block and 'transactions' in block:
            for tx in block['transactions']:
                if tx['from'] == account or tx['to'] == account:
                    transactions.append(tx)

        print(f"scanned block {block_number}")

    return transactions


if __name__ == "__main__":
    load_config()
    config = get_config()
    print("config loaded:", config)
    account = config['SENDER_WALLET']
    latest_block = get_latest_Block_number()
    start_block = latest_block - 100

    transactions = find_transactions_by_account(account, start_block, latest_block)
    for tx in transactions:
        print(f"Transaction Hash: {tx['hash']}")
        print(f"From: {tx['from']} To: {tx.get('to', 'Contract Creation')}")
        print(f"Value: {int(tx['value'], 16) / 10**18} ETH")
        print(f"Block Number: {int(tx['blockNumber'], 16)}")