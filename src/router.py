from src.utils.Blockchain_functions import *

def transaction_router(intent):
    """
    This function routes the transaction based on the intent

    :param intent:
    :return:
    """
    transaction_type = intent['intent'].get('transaction_type') or intent['intent'].get('type')

    if not transaction_type:
        raise ValueError("Transaction type is missing in the intent")

    # Using match-case
    match transaction_type:
        case 'TRANSFER':
            return execute_eth_tranasfer(intent['intent'])
        case 'TRANSFER_ERC20':
            return execute_erc20_transfer(intent['intent'])
        case 'SWAP_EXACT_ETH_FOR_TOKENS':
            return execute_swapExactETHForTokens(intent['intent'])
        case 'WRAP':
            return execute_wrap_eth(intent['intent'])
        case 'UNWRAP':
            return execute_unwrap_eth(intent['intent'])
        case _:
            raise ValueError(f"Unknown transaction type {transaction_type}")
