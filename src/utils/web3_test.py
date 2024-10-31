from datetime import datetime, timedelta

from web3 import Web3
import json
from config import load_config, get_config
load_config()
config = get_config()


if __name__ == "__main__":
    load_config()
    config = get_config()
    print("config loaded:", config)
# Connect to the Hardhat fork
infura_url = config['NETWORK_URL']
w3 = Web3(Web3.HTTPProvider(infura_url))

# Check connection
if not w3.is_connected():
    raise ConnectionError("Failed to connect to the Ethereum node")

# Load Uniswap V2 Router ABI
with open('../../data/uniswap_v2_router_abi.json') as f:
    uniswap_v2_router_abi = json.load(f)
uniswap_v2_router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'

# Create contract instance
uniswap_v2_router = w3.eth.contract(address=uniswap_v2_router_address, abi=uniswap_v2_router_abi)

# Load wallet
private_key = '0x47c99abed3324a2707c28affff1267e45918ec8c3f20b8aa892e8b065d2942dd'
account = w3.eth.account.from_key(private_key)
address = account.address

# Define swap parameters
eth_amount = w3.to_wei(10, 'ether')
usdc_amount_min = w3.to_wei(1000, 'mwei')
path = ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', config['USDC_CONTRACT']]
deadline = int((datetime.utcnow() + timedelta(minutes=10)).timestamp())
nonce = w3.eth.get_transaction_count(address)


# Build the swap transaction
transaction = uniswap_v2_router.functions.swapExactETHForTokens(
    usdc_amount_min,
    path,
    address,
    deadline
).build_transaction({
    'from': address,
    'value': eth_amount,
    'gas': 200000,
    'gasPrice': w3.to_wei('20', 'gwei'),
    'nonce': nonce,
})

signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)

transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

print(f'Transaction hash: {w3.to_hex(transaction_hash)}')

receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print(f'Transaction confirmed in block: {receipt.blockNumber}')
