from datetime import datetime, timedelta
from typing import Optional

from web3 import Web3
import json
import logging
from config import load_config, get_config
import os

PK = os.getenv('PK') #PK = config['PK']

load_config()
config = get_config()

w3 = Web3(Web3.HTTPProvider(config['NETWORK_URL']))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_latest_block():
    """
    Fetch the latest block from the Ethereum network.

    Returns:
    - dict: A dictionary containing the latest block's details.
    """
    block_number = w3.eth.block_number  # Get the latest block number
    block = w3.eth.get_block(block_number)  # Fetch the latest block details
    return block

def calc_base_fee_of_next_block():
    """
    Calculate the base fee of the next block based on the parent block.

    Args:
    - parent_block (dict): A dictionary containing the parent block's details.

    Returns:
    - int: The calculated base fee for the next block in Gwei.
    """

    parent_block = get_latest_block()
    # Constants for calculation
    ElasticityMultiplier = 2  # EIP-1559 The block size has been expanded, the maximum multiple is 2
    BaseFeeChangeDenominator = 8  # The amount the base fee can change between blocks

    parent_gas_target = parent_block['gasLimit'] // ElasticityMultiplier
    gas_used = parent_block['gasUsed']
    base_fee_per_gas = parent_block['baseFeePerGas']

    if gas_used == parent_gas_target:
        # Parent block's gasUsed is the same as the target, baseFee remains unchanged
        return base_fee_per_gas
    if gas_used > parent_gas_target:
        # Parent block uses gas greater than the target value, baseFee increase
        gas_used_delta = gas_used - parent_gas_target
        base_fee_delta = max(
            (base_fee_per_gas * gas_used_delta) // parent_gas_target // BaseFeeChangeDenominator,
            1
        )
        return base_fee_per_gas + base_fee_delta
    else:
        # The gas used by the parent block is less than the target value, baseFee reduce
        gas_used_delta = parent_gas_target - gas_used
        base_fee_delta = (base_fee_per_gas * gas_used_delta) // parent_gas_target // BaseFeeChangeDenominator
        return max(base_fee_per_gas - base_fee_delta, 0)

def calculate_final_gas_price(tip_percentage):
    """
    Calculate the final gas price based on the parent block's base fee and a percentage tip.

    Args:
    - tip_percentage (float): The percentage to calculate the tip from the base fee.

    Returns:
    - int: The total gas price in Gwei.
    """

    # Calculate base fee
    base_fee = calc_base_fee_of_next_block()

    # Calculate tip based on the specified percentage of the base fee
    tip = int(base_fee * tip_percentage / 100)

    # Calculate total gas price
    gas_price = base_fee + tip
    return gas_price

def build_transaction_params(account, nonce, intent):
    # gas_price = calculate_final_gas_price( tip_percentage=10)

    return{
        'from': account.address,
        'gas': int(config['GAS_LIMIT'], 16),
        'gasPrice':int(config['GAS_PRICE'], 16),    #gas_price,
        'nonce': nonce,
        'chainId': 1313161555

    }



#TODO: Fix issues with swapEThForExactTokens -----> Done
def execute_swapEthForExactTokens(intent):
    try:
        account = w3.eth.account.from_key(PK)
        address = account.address
        nonce = w3.eth.get_transaction_count(address)
        uniswap_v2_router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'

        with open('uniswap_v2_router_abi.json') as f:
            uniswap_v2_router_abi = json.load(f)


        uniswap_v2_router = w3.eth.contract(address = w3.to_checksum_address(uniswap_v2_router_address), abi = uniswap_v2_router_abi)
        deadline = int((datetime.utcnow() + timedelta(minutes=10)).timestamp())
        path = [intent['token_in'], intent['token_out']]
        transaction = uniswap_v2_router.functions.swapETHForExactTokens(
            int(intent['amount_out']),
            path,
            address,
            deadline
        ).build_transaction({
            **build_transaction_params(account, nonce),
            'value': w3.to_wei(intent['amount_in_max_eth'], 'ether')
        })

        # receipt = sign_and_send_transaction(transaction, config['PK'], w3)
        logger.info("Swap ETH for tokens  executed successfully")
        return transaction
    except Exception as e:
        logger.error("Failed to execute swap ETH for tokens")
        logger.error(e)
        return None




def execute_eth_tranasfer(intent):
    try:
        account = w3.eth.account.from_key(PK)
        address = account.address
        nonce = w3.eth.get_transaction_count(address)

        transaction = {
            **build_transaction_params(account, nonce, intent),
            "to": intent['to'],
            "value":  w3.to_wei(intent['amount'], 'ether')
        }
        print(transaction)
        # receipt = sign_and_send_transaction(transaction, config['PK'], w3)
        logger.info("ETH transfer executed successfully")
        return transaction
    except Exception as e:
        logger.error("Failed to execute ETH transfer")
        logger.error(e)
        return None


TOKEN_CONTRACT_ADDRESSES = {
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC contract on Ethereum mainnet
    "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",   # DAI contract on Ethereum mainnet
    "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH contract on Ethereum mainnet
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT contract on Ethereum mainnet
    "PEPE": "0x6982508145454Ce325dDbE47a25d4ec3d2311933"   # PEPE contract on Ethereum mainnet
}
def resolve_token_address(token_symbol: str) -> Optional[str]:
    """Resolve the token contract address based on the token symbol."""
    return TOKEN_CONTRACT_ADDRESSES.get(token_symbol.upper())

def execute_erc20_transfer(intent):
    try:
        account = w3.eth.account.from_key(PK)
        address = account.address
        nonce = w3.eth.get_transaction_count(address)
        with open('erc20.abi.json') as f:
            erc20_abi = json.load(f)

        token_contract_address = resolve_token_address(intent.get('token_symbol'))   #or intent.get('token_contract')

        if not token_contract_address:
            raise ValueError("Token contract address could not be resolved")
        # token_contract = w3.eth.contract(address=w3.to_checksum_address(intent['token_contract']), abi=erc20_abi)
        token_contract = w3.eth.contract(address=w3.to_checksum_address(token_contract_address), abi=erc20_abi)
        transaction = token_contract.functions.transfer(
            intent['to'],
            int(intent['amount']) * 10 ** 6
        ).build_transaction({
            **build_transaction_params(account, nonce)
        })
        # receipt = sign_and_send_transaction(transaction, config['PK'], w3)
        logger.info("ERC20 transfer executed successfully")
        return transaction
    except Exception as e:
        logger.error("Failed to execute ERC20 transfer")
        logger.error(e)
        return None


def execute_swapExactETHForTokens(intent):
    try:
        account = w3.eth.account.from_key(PK)
        address = account.address
        nonce = w3.eth.get_transaction_count(address)

        uniswap_v2_router_address = w3.to_checksum_address('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
        with open('uniswap_v2_router_abi.json') as f:
            uniswap_v2_router_abi = json.load(f)

        uniswap_v2_router = w3.eth.contract(address=uniswap_v2_router_address, abi=uniswap_v2_router_abi)
        deadline = int((datetime.utcnow() + timedelta(minutes=10)).timestamp())
        path = [w3.to_checksum_address(intent['token_in']), w3.to_checksum_address(intent['token_out'])]

        transaction = uniswap_v2_router.functions.swapExactETHForTokens(
            0,
            path,
            address,
            deadline
        ).build_transaction({
            **build_transaction_params(account, nonce),
            'value': w3.to_wei(intent['amount_in_eth'], 'ether')
        })

        # receipt = sign_and_send_transaction(transaction, config['PK'], w3)
        logger.info("Swap transaction executed successfully")
        return transaction
    except Exception as e:
        logger.error("Failed to execute swap transaction")
        logger.error(e)
        return None


def execute_wrap_eth(intent):
    try:
        account = w3.eth.account.from_key(PK)
        address = account.address
        nonce = w3.eth.get_transaction_count(address)
        weth_contract_address = w3.to_checksum_address(config['WETH_CONTRACT'])
        with open('weth_abi.json') as f:
           weth_abi = json.load(f)


        weth_contract = w3.eth.contract(address=weth_contract_address, abi=weth_abi)
        transaction = weth_contract.functions.deposit().build_transaction({
            **build_transaction_params(account, nonce),
            'value': w3.to_wei((intent['amount']), 'ether')
        })
        # receipt = sign_and_send_transaction(transaction, config['PK'], w3)
        logger.info("Wrap ETH executed successfully")
        return transaction

    except Exception as e:
        logger.error("Failed to execute wrap ETH")
        logger.error(e)
        return None


def execute_unwrap_eth(intent):
    try:
        account = w3.eth.account.from_key(PK)
        address = account.address
        nonce = w3.eth.get_transaction_count(address)
        weth_contract_address = w3.to_checksum_address(config['WETH_CONTRACT'])

        with open('weth_abi.json') as f:
            weth_abi = json.load(f)

        weth_contract = w3.eth.contract(address=weth_contract_address, abi=weth_abi)
        transaction = weth_contract.functions.withdraw(
            w3.to_wei((intent['amount']), 'ether')).build_transaction({
            **build_transaction_params(account, nonce)
        })
        # receipt = sign_and_send_transaction(transaction, config['PK'], w3)
        logger.info("Unwrap ETH executed successfully")
        return transaction
    except Exception as e:
        logger.error("Failed to execute unwrap ETH")
        logger.error(e)
        return None



# def execute_swapExactETHForTokens_transaction(intent):
#     try:
#         account = w3.eth.account.from_key(config['PK'])
#         address = account.address
#         nonce = w3.eth.get_transaction_count(address)
#
#         uniswap_v2_router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
#         with open('uniswap_v2_router_abi.json') as f:
#             uniswap_v2_router_abi = json.load(f)
#
#         uniswap_v2_router = w3.eth.contract(address =w3.to_checksum_address(uniswap_v2_router_address) , abi = uniswap_v2_router_abi)
#         deadline = int((datetime.utcnow() + timedelta(minutes=10)).timestamp())
#         path = [intent['token_in'], intent['token_out']]
#
#         transaction = uniswap_v2_router.functions.swapExactETHForTokens(
#             0,
#             path,
#             address,
#             deadline
#         ).build_transaction({
#             **build_transaction_params(account, nonce),
#             'value': w3.to_wei(intent['amount_in_eth'], 'ether')
#         })
#
#         # receipt = sign_and_send_transaction(transaction, config['PK'], w3)
#         logger.info("Swap transaction executed successfully")
#         return transaction
#     except Exception as e:
#         logger.error("Failed to execute swap transaction")
#         logger.error(e)
#         return None


def Create_wallet(intent):
    #TODO: Implement wallet creation
    pass




