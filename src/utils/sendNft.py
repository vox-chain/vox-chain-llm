from web3 import Web3
import json
from config import load_config, get_config

load_config()
config = get_config()
# Connect to the local Hardhat fork
def connect_to_eth_fork():
    web3 = Web3(Web3.HTTPProvider(config['NETWORK_URL']))
    if web3.is_connected():
        print("Connected to Ethereum fork")
    else:
        raise ConnectionError("Failed to connect to Ethereum fork")
    return web3


# Impersonate an account on the fork (specific to Hardhat)
def impersonate_account(web3, address):
    web3.provider.make_request("hardhat_impersonateAccount", [address])
    return address


# Build the transaction to transfer the NFT
def build_nft_transfer_transaction(web3, nft_contract, from_address, to_address, token_id):
    # Create the transaction object
    tx = nft_contract.functions.safeTransferFrom(
        from_address,
        to_address,
        token_id
    ).build_transaction({
        'from': from_address,
        'nonce': web3.eth.get_transaction_count(from_address),
        'gas': 2000000,  # Adjust gas limit as necessary
        'gasPrice': web3.to_wei('1000', 'gwei')
    })
    return tx


# Sign and send the transaction
def sign_and_send_transaction(web3, tx, private_key):
    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(f"Transaction successful with hash: {tx_hash.hex()}")
    return receipt


# Get the current owner of the NFT
def get_nft_owner(nft_contract, token_id):
    return nft_contract.functions.ownerOf(token_id).call()


# Main function to execute the transfer based on intent
def send_nft(intent, web3):
    # Extract intent details
    transaction_type = intent['intent']['transaction_type']
    nft_contract_address = intent['intent']['nft_contract']
    token_id = int(intent['intent']['token_id'])
    to_address = intent['intent']['to']

    if transaction_type != 'TRANSFER_NFT':
        raise ValueError("Invalid transaction type")

    # Load the ERC-721 ABI from a JSON file (make sure you have erc721-ai.json)
    with open('../../data/erc721-abi.json') as f:
        erc721_abi = json.load(f)

    # Load the NFT contract
    nft_contract = web3.eth.contract(address=Web3.to_checksum_address(nft_contract_address), abi=erc721_abi)

    # Get the current owner of the NFT
    current_owner = get_nft_owner(nft_contract, token_id)
    print(f"Current owner of token {token_id}: {current_owner}")

    # Impersonate the NFT holder
    impersonated_account = impersonate_account(web3, current_owner)

    # Build the transaction
    tx = build_nft_transfer_transaction(web3, nft_contract, impersonated_account, to_address, token_id)

    # Send the transaction without requiring a private key since we're impersonating
    tx_hash = web3.eth.send_transaction(tx)

    # Wait for the transaction receipt
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction successful with hash: {tx_hash.hex()}")

    # Verify the transfer
    new_owner = get_nft_owner(nft_contract, token_id)
    print(f"New owner of token {token_id}: {new_owner}")



if __name__ == "__main__":
    # Example intent
    intent = {
        'intent': {
            'transaction_type': 'TRANSFER_NFT',
            'nft_contract': '0xED5AF388653567Af2F388E6224dC7C4b3241C544',
            'token_id': '124',
            'to': '0x1234567890123456789012345678901234567890'
        },
        'chain': '1'
    }

    # Connect to the Ethereum fork
    web3 = connect_to_eth_fork()

    # Execute the NFT transfer based on the intent
    send_nft(intent, web3)
