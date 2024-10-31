from rpc_templates import create_native_transfer_tranaction, create_erc20_transfer_transaction, create_swap_eth_for_tokens_transaction

def handle_transaction(intent):

    if intent['transaction_type'] == 'TRANSFER':
        return create_native_transfer_tranaction(intent)
    elif intent['transaction_type'] == 'TRANSFER_ERC20':
        return create_erc20_transfer_transaction(intent)
    elif intent['transaction_type'] == 'SWAP_EXACT_ETH_FOR_TOKENS':
        return create_swap_eth_for_tokens_transaction(intent)
    else:
        raise ValueError(f"Unknown transaction type {intent['type']}")