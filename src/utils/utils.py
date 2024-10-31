import hashlib
from decimal import Decimal, getcontext

getcontext().prec = 100

def kecca256(data: bytes) -> bytes:
    return hashlib.sha3_256(data).digest()


def calculate_data_field(to_address: str, amount: float,token_decimals:int) ->str:
    """
    Calculate the data field for ERC20 transactions
    """
    to_address = to_address.lower().replace('0x', '')
    amount = int(Decimal(amount) * Decimal(10**token_decimals))
    amount_hex = hex(amount)[2:]
    methode_id = '0xa9059cbb'
    padded_to_address = '0' * (64 - len(to_address)) + to_address
    padded_amount = '0' * (64 - len(amount_hex)) + amount_hex
    data_field = methode_id + padded_to_address + padded_amount

    return data_field

def calculate_approve_data_field(spender: str, amount: str) -> str:
    """
    Calculate the data field for an approve transaction.
    """
    method_id = '0x095ea7b3'  # approve(address,uint256) function selector

    spender_padded = spender.lower().replace('0x', '').zfill(64)

    amount_int = int(amount)
    amount_hex = hex(amount_int)[2:].zfill(64)

    data_field = method_id + spender_padded + amount_hex

    return data_field

def calculate_swap_data_field(amount_out_min: str, token_in: str,token_out: str, recipient: str )->str:
    """
    Calculate the data field for swap transactions
    """
    method_id = '0x7ff36ab5'
    amount_out_min_int = int(Decimal(amount_out_min))
    amount_out_min_hex = hex(amount_out_min_int)[2:].zfill(64)

    token_in = token_in.lower().replace('0x', '').zfill(64)
    token_out = token_out.lower().replace('0x', '').zfill(64)
    recipient = recipient.lower().replace('0x', '').zfill(64)

    path = token_in + token_out
    deadline = hex(1666625485)[2:].zfill(64)

    data_field = method_id + amount_out_min_hex + path + recipient + deadline

    return data_field

