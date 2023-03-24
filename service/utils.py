from web3 import Web3

from service.creds import HTTP_NODE
from service.engine.contracts.uniswap_v3 import UniswapV3Connector
from service.models import Token


def get_ethusd_price(amount: float) -> float:
    """Returns WETH/USDC price from Uniswap V3 0.05% pool.

    Args:
        amount (float): amount ETH to swap

    Returns:
        float: price
    """
    node = Web3(Web3.HTTPProvider(HTTP_NODE))
    pool = UniswapV3Connector(
        node=node,
        zfo=True,
        token0=Token(address='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                     decimals=18, symbol='WETH'),
        token1=Token(address='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                     decimals=6, symbol='USDC'),
        fees=0.0005,
    )
    amount_out = pool.get_amount_out(amount_in=amount)
    return amount_out / amount
