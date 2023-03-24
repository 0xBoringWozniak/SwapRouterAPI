from enum import Enum


class DEX(Enum):
    """
    Enum for DEXes.
    """
    UNISWAP_V3 = 'uniswap_v3'
    UNISWAP_V2 = 'uniswap_v2'
    CURVE = 'curve'


class Notional(Enum):
    """
    For now, we only support USDC/WETH.
    """
    WETH = 'weth'
    USDC = 'usdc'
