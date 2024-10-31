from config import get_config, load_config
from utils import calculate_data_field, calculate_swap_data_field



def create_native_transfer_tranaction(intent):
    load_config()
    config = get_config()
    return {
        "jsonrpc": "2.0",
        "method": "eth_sendTransaction",
        "params": [
            {
                "from":config['SENDER_WALLET'],
                "to": intent['to'],
                "value": intent['amount'],
                "gas": config['GAS_LIMIT'],
                "gasPrice": config['GAS_PRICE'],
            }],
        "id": 1,
    }

def create_wrap_eth_transaction(intent):
    load_config()
    config = get_config()

    return {
        "jsonrpc": "2.0",
        "method": "eth_sendTransaction",
        "params": [
            {
                "from": config['SENDER_WALLET'],
                "to": config['WETH_CONTRACT'],
                "value": intent['amount'],
                "gas": config['GAS_LIMIT'],
                "gasPrice": config['GAS_PRICE'],
            }],
        "id": 1,
    }

def create_erc20_transfer_transaction(intent):
    load_config()
    config = get_config()
    data_field = calculate_data_field(intent['to'], intent['amount'], 6)

    return {
        "jsonrpc": "2.0",
        "method": "eth_sendTransaction",
        "params": [
            {
                "from":config['SENDER_WALLET'],
                "to": config['USDC_CONTRACT'],
                "data":data_field ,
                "gas": config['GAS_LIMIT'],
                "gasPrice": config['GAS_PRICE'],
            }],
        "id": 1,
    }


def create_swap_eth_for_tokens_transaction(intent):
    load_config()
    config = get_config()
    data_field = calculate_swap_data_field(
        '0',
        intent['token_in'],
        intent['token_out'],
        config['SENDER_WALLET'],

    )
    return {
        "jsonrpc": "2.0",
        "method": "eth_sendTransaction",
        "params": [
            {
                "from":config['SENDER_WALLET'],
                "to": intent['contract_address'],
                "data":data_field,
                "value": hex(int(intent['amount_in_eth']) * (10 ** 18)),
                "gas": config['GAS_LIMIT'],
                "gasPrice": config['GAS_PRICE'],
            }],
        "id": 1,
    }

if __name__ == "__main__":

    load_config()
    config = get_config()
    print(config)
    intent = {'type': 'TRANSFER_ERC20', 'to': '0xcd3B766CCDd6AE721141F452C550Ca635964ce71', 'value': 10}
    print(create_erc20_transfer_transaction(intent))
    intent = {'type': 'TRANSFER', 'to': '0xcd3B766CCDd6AE721141F452C550Ca635964ce72', 'value': 10}
    print(create_native_transfer_tranaction(intent))
    intent = {'amount_in_eth': '1', 'amount_out_min': '950',
             'contract_address': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',
             'to': '0x5AEDA56215b167893e80B4fE645664366c514bAb',
             'token_in': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
             'token_out': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'transaction_type': 'SWAP_EXACT_ETH_FOR_TOKENS'}
    print(create_swap_eth_for_tokens_transaction(intent))