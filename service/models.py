import typing as tp

from pydantic import BaseModel

from service.enums import DEX, Notional


class Error(BaseModel):
    """
    Base error model for all errors in the API.
    """
    error_key: str
    error_message: str
    error_loc: tp.Optional[tp.Any] = None


class Trade(BaseModel):
    """
    Trade entity.
    """
    amount: float                                   # amount of token_in
    token_in_symbol: str                            # token_in symbol (e.g. USDT)
    excluded_dexes: tp.Optional[tp.Set[DEX]] = set() # excluded dexes (e.g. UniswapV2)


class Token(BaseModel):
    """
    Token entity (ERC20).
    """
    address: str            # token ethereum address
    decimals: int           # token decimals (used to save RPC calls)
    symbol: str             # token symbol (e.g. USDT)


class Pool(BaseModel):
    """
    Pool entity.
    """
    address: str            # pool ethereum address
    dex: DEX                # dex type (e.g. UniswapV2)
    notional: Notional      # notional type (e.g. usdc/weth)
    zfo: int                # is zfo pool (for curve i,y indexes in 2 digits)
    fees: float             # pool fees (e.g. 0.003)
    token0: Token           # token0 in pool
    token1: Token           # token1 in pool

    # make it hashable to store in set/dict
    def __hash__(self):
        return hash(self.address)


class TradeStats(BaseModel):
    """
    Trade stats.
    """
    amount_out: float           # amount of token_out
    amount_out_in_usd: float    # amount of token_out in usd


class PoolWithTradeStats(BaseModel):
    """
    Pool with trade stats.
    """
    pool: Pool
    trade_stats: TradeStats
