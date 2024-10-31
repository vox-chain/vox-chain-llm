from pydantic import BaseModel, Field, ValidationError
from typing import Union, Literal, Optional


# Define individual transaction intent classes with examples
class TransferIntent(BaseModel):
    transaction_type: Literal["TRANSFER"] = "TRANSFER"
    amount: float = Field(..., title="Amount", description="The amount of native token to transfer", examples=[0.1, 1, 10])
    to: str = Field(..., title="To", description="The address to receive the native token", examples=["0x1234567890123456789012345678901234567890"])

    class Config:
       schema_extra = {
            "example": {
                "transaction_type": "TRANSFER",
                "amount": 1.0,
                "to": "0x1234567890123456789012345678901234567890"
            }
        }

class TransferERC20Intent(BaseModel):

    transaction_type: Literal["TRANSFER_ERC20"] = "TRANSFER_ERC20"
    token_contract: str = Field(..., title="Token Contract", description="The ERC-20 token contract address", examples=["0xabcdef1234567890abcdef1234567890abcdef12"])
    token_symbol: str = Field(None, title="Token Symbol", description="The symbol of the ERC-20 token", examples=["USDC", "DAI"])

    amount: float = Field(..., title="Amount", description="The amount of ERC-20 tokens to transfer", examples=[10, 50, 100])
    to: str = Field(..., title="To", description="The address to receive the ERC-20 token", examples=["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48, 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2,0xdAC17F958D2ee523a2206206994597C13D831ec7"])

    class Config:
        schema_extra = {
            "example": {
                "transaction_type": "TRANSFER_ERC20",
                "token_contract": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "token_symbol": "USDC",
                "amount": 10.0,
                "to": "0x1234567890123456789012345678901234567890"
            }
        }


class SwapExactEthForTokensIntent(BaseModel):
    transaction_type: Literal["SWAP_EXACT_ETH_FOR_TOKENS"] = "SWAP_EXACT_ETH_FOR_TOKENS"
    contract_address: str = Field(..., title="Contract Address", description="The address of the contract for Uniswap_v2", examples=["0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"])
    token_out: str = Field(..., title="Token Out", description="The token being received", examples=["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"])
    token_in: str = Field(..., title="Token In", description="The token being swapped from", examples=["0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"])
    amount_in_eth: float = Field(..., title="Amount In ETH", description="The exact amount of ETH to swap", examples=[0.1, 1, 5])
    amount_out_min: float = Field(..., title="Amount Out Min", description="The minimum amount of token_out expected", examples=[10, 50, 100])
    # to: str = Field(..., title="To", description="The address to receive the token_out", examples=["0x1234567890123456789012345678901234567890"])
    class Config:
        schema_extra = {
            "example": {
                "transaction_type": "SWAP_EXACT_ETH_FOR_TOKENS",
                "contract_address": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
                "token_out": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "token_in": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                "amount_in_eth": 1.0,
                "amount_out_min": 10.0
            }
        }



class WrapIntent(BaseModel):
    transaction_type: Literal["WRAP"] = "WRAP"
    amount: float = Field(..., title="Amount", description="The amount of ETH to wrap", examples=[0.1, 1, 5])

    class Config:
        schema_extra = {
            "example": {
                "transaction_type": "WRAP",
                "amount": 1.0
            }
        }

class UnwrapIntent(BaseModel):
    transaction_type: Literal["UNWRAP"] = "UNWRAP"
    amount: float = Field(..., title="Amount", description="The amount of WETH to unwrap", examples=[0.1, 1, 5])

    class Config:
        schema_extra = {
            "example": {
                "transaction_type": "UNWRAP",
                "amount": 1.0
            }
        }


class TransferNFTIntent(BaseModel):
    transaction_type: Literal["TRANSFER_NFT"] = "TRANSFER_NFT"
    nft_contract: str = Field(..., title="NFT Contract Address", description="The NFT contract address", examples=["0xABCDEF1234567890ABCDEF1234567890ABCDEF12"])
    token_id: str = Field(..., title="Token ID", description="The ID of the NFT to transfer", examples=["1234"])
    to: str = Field(..., title="To", description="The address to receive the NFT", examples=["0x1234567890123456789012345678901234567890"])

    class Config:
        schema_extra = {
            "example": {
                "transaction_type": "TRANSFER_NFT",
                "nft_contract": "0xABCDEF1234567890ABCDEF1234567890ABCDEF12",
                "token_id": "1234",
                "to": "0x1234567890123456789012345678901234567890"
            }
        }



class BridgeIntent(BaseModel):
    transaction_type: Literal["BRIDGE"] = "BRIDGE"
    token: str = Field(..., title="Token", description="The token to bridge (e.g., ETH, USDC, DAI)", examples=["ETH", "USDC"])
    amount: float = Field(..., title="Amount", description="The amount of the token to bridge", examples=[0.1, 10, 100])
    destination_chain: str = Field(..., title="Destination Chain", description="The blockchain to which the token is being bridged", examples=["Polygon", "Avalanche", "BSC"])
    to: str = Field(..., title="To", description="The recipient address on the destination chain", examples=["0x1234567890123456789012345678901234567890"])

    class Config:
        schema_extra = {
            "example": {
                "transaction_type": "BRIDGE",
                "token": "ETH",
                "amount": 1.0,
                "destination_chain": "Polygon",
                "to": "0x1234567890123456789012345678901234567890"
            }
        }

class TransactionIntent(BaseModel):
    """
    This class represents a generic transaction intent
    """
    intent: Union[TransferIntent, TransferERC20Intent, WrapIntent, UnwrapIntent, SwapExactEthForTokensIntent, TransferNFTIntent]
    chain : Optional[str] = Field(..., title="Chain", description="The ID of the blockchain network to execute the transaction on", examples=["1", "56", "43114"])