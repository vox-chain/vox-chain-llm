from web3 import Web3

from web3 import Web3
import json
import logging
from config import load_config, get_config

load_config()
config = get_config()

w3 = Web3(Web3.HTTPProvider(config['NETWORK_URL']))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def verify_erc20_contract(token_contract_address):
    # Load the contract using the token contract address and the ERC-20 ABI
    with open('/data/erc20.abi.json') as f:
        erc20_abi = json.load(f)
    token_contract = w3.eth.contract(address=Web3.to_checksum_address(token_contract_address), abi=erc20_abi)

    try:
        # Check if we can get the name, symbol, and decimals
        name = token_contract.functions.name().call()
        symbol = token_contract.functions.symbol().call()
        decimals = token_contract.functions.decimals().call()

        print(f"Token Name: {name}")
        print(f"Token Symbol: {symbol}")
        print(f"Token Decimals: {decimals}")
        return True  # If all these work, the contract is likely valid

    except Exception as e:
        print(f"Error verifying contract: {e}")
        return False  # If any of these fail, the contract may not be a valid ERC-20 contract

if __name__ == "__main__":
    token_contract_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    if verify_erc20_contract(token_contract_address):
        print("Contract is valid ERC-20")
    else:
        print("Invalid contract")