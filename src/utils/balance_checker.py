import json
import requests
from config import load_config, get_config

load_config()
config = get_config()
headers = {'Content-Type': 'application/json'}


def call_contract(contract_address, function_signature, params):
    rpc_call = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{
            "to": contract_address,
            "data": function_signature + params
        }, "latest"],
        "id": 1
    }
    response = requests.post(config['NETWORK_URL'], headers=headers, data=json.dumps(rpc_call))
    if response.status_code == 200:
        return response.json()['result']
    else:
        print('Failed to call the contract', response.text)
        return None


def get_eth_balance(address):
    """
    Get the ETH balance of an address
    :param address:
    :return: ETH balance
    """
    rpc_call = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    response = requests.post(config['NETWORK_URL'], headers=headers, data=json.dumps(rpc_call))
    if response.status_code == 200:
        balance_wei = response.json()['result']
        return int(balance_wei, 16)
    else:
        print('Failed to get ETH balance', response.text)
        return None


def get_weth_balance(address):
    """
    Get the WETH balance of an address
    :param address:
    :return:  WETH balance
    """
    function_signature = "0x70a08231"  # balanceOf(address) function signature
    address_hex = address.lower().replace('0x', '').zfill(64)
    params = address_hex
    result = call_contract(config['WETH_CONTRACT'], function_signature, params)
    if result:
        return int(result, 16)
    else:
        return None


def get_usdc_balance(address):
    """
    Get the USDC balance of an address
    :param address:
    :return: USDC balance
    """
    function_signature = "0x70a08231"  # balanceOf(address) function signature
    address_hex = address.lower().replace('0x', '').zfill(64)
    params = address_hex
    result = call_contract(config['USDC_CONTRACT'], function_signature, params)
    if result:
        return int(result, 16)
    else:
        return None


def get_all_balances(address):
    """
    Get the ETH, WETH and USDC balances of an address
    :param address:
    :return: all balances
    """
    eth_balance = get_eth_balance(address) / 10 ** 18
    weth_balance = get_weth_balance(address) / 10 ** 18
    usdc_balance = get_usdc_balance(address) / 10 ** 6
    return eth_balance, weth_balance, usdc_balance



if __name__ == "__main__":
    load_config()
    config = get_config()
    print("Config loaded:", config)
    address = config['SENDER_WALLET']

    # Get balances
    eth_balance = get_eth_balance(address) / 10 ** 18
    weth_balance = get_weth_balance(address) / 10 ** 18
    usdc_balance = get_usdc_balance(address) / 10 ** 6

    # Print balances
    print(f"ETH balance of {address} is {eth_balance} ETH")
    print(f"WETH balance of {address} is {weth_balance} WETH")
    print(f"USDC balance of {address} is {usdc_balance} USDC")
