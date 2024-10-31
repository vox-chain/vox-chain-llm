import requests
import json
from config import load_config, get_config

load_config()
config = get_config()
def impersonate_account(address):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(config['NETWORK_URL'], headers=headers, data=json.dumps({
        "jsonrpc": "2.0",
        "method": "hardhat_impersonateAccount",
        "params": [address],
        "id": 1
    }))
    if response.status_code != 200:
        raise Exception('Failed to impersonate account', response.text)



def stop_impersonating_account(address):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(config['NETWORK_URL'], headers=headers, data=json.dumps({
        "jsonrpc": "2.0",
        "method": "hardhat_stopImpersonatingAccount",
        "params": [address],
        "id": 1
    }))
    if response.status_code != 200:
        raise Exception('Failed to stop impersonating account', response.text)

def execute_transaction(rpc_transaction):

    network_url = config['NETWORK_URL']
    impersonate_account(config['SENDER_WALLET'])
    headers = {'Content-Type': 'application/json'}
    response = requests.post(network_url, headers=headers, data=json.dumps(rpc_transaction))
    if response.status_code == 200:
        return response.json()
    else:
        print('transaction failed', response.text)

    stop_impersonating_account(config['SENDER_WALLET'])





def fund_account():
    transaction = {
        "jsonrpc": "2.0",
        "method": "eth_sendTransaction",
        "params": [{
            "from": "0xcd3B766CCDd6AE721141F452C550Ca635964ce71",
            "to": "0x1CBd3b2770909D4e10f157cABC84C7264073C9Ec",
            "value": hex(100 * 10**18),
        }],
        "id": 1
    }

    network_url = config['NETWORK_URL']
    headers = {'Content-Type': 'application/json'}

    # Send the transaction
    response = requests.post(network_url, headers=headers, data=json.dumps(transaction))
    if response.status_code == 200:
        return response.json()
    else:
        print('Funding transaction failed', response.text)

def get_balance(network_url):
    rpc_call = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [config['SENDER_WALLET'], "latest"],
        "id": 1
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(network_url, headers=headers, data=json.dumps(rpc_call))
    if response.status_code == 200:
        balance_wei = response.json()['result']
        return int(balance_wei, 16)/ 10 ** 18
    else:
        print('Failed to get ETH balance', response.text)
        return None
