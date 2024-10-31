from web3 import Web3
from config import load_config, get_config

load_config()
config = get_config()

w3 = Web3(Web3.HTTPProvider(config['NETWORK_URL']))
eth_json_rpc_endpoint = config['NETWORK_URL']
ElasticityMultiplier = 2  # EIP-1559 The block size has been expanded, the maximum multiple is 2
BaseFeeChangeDenominator = 8  # The amount the base fee can change between blocks

def calc_base_fee_of_next_block(parent_block):
    parent_gas_target = parent_block.gasLimit // ElasticityMultiplier
    print('parent_gas_target', parent_gas_target)
    print('parent_block.gasUsed', parent_block.gasUsed)
    print('parent_block.baseFeePerGas', parent_block.baseFeePerGas)
    if parent_block.gasUsed == parent_gas_target:
        # parent block's gasUsed is the same as the target, baseFee remains unchanged
        return parent_block.baseFeePerGas
    if parent_block.gasUsed > parent_gas_target:
        # parent block uses gas greater than the target value, baseFee increase
        gas_used_delta = parent_block.gasUsed - parent_gas_target
        x = parent_block.baseFeePerGas * gas_used_delta
        y = x // parent_gas_target
        base_fee_delta = max(
            y // BaseFeeChangeDenominator,
            1
        )
        return parent_block.baseFeePerGas + base_fee_delta
    else:
        # the gas used by the parent block is less than the target value, baseFee reduce
        gas_used_delta = parent_gas_target - parent_block.gasUsed
        x = parent_block.baseFeePerGas * gas_used_delta
        y = x // parent_gas_target
        base_fee_delta = y // BaseFeeChangeDenominator
        return max(
            parent_block.baseFeePerGas - base_fee_delta,
            0
        )


if __name__ == '__main__':
    ethClient = Web3(Web3.HTTPProvider(eth_json_rpc_endpoint))
    block_number = ethClient.eth.block_number
    block = ethClient.eth.get_block(block_number)

    base_fee_of_next_block = calc_base_fee_of_next_block(block)
    print(f"Base fee for block {block_number + 1} will be {base_fee_of_next_block}")


