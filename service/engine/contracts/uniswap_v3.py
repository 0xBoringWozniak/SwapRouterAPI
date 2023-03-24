from web3 import Web3

from service.models import Token
from service.engine.contracts.connector import Connector
from service.engine.contracts.abis import UNISWAP_V3_QUOTER_ABI


class UniswapV3Connector(Connector):

    # Uniswap V3 Quoter contract ABI and address    
    ABI = UNISWAP_V3_QUOTER_ABI
    ADDRESS = '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6'

    def __init__(
            self,
            node: Web3,
            zfo: bool,
            token0: Token,
            token1: Token,
            fees: float,
        ) -> None:
        """
        Uniswap V3 connector. Uses Uniswap V3 Quoter contract. quoteExactInputSingle is used for getting amount out.

        Args:
            node (Web3): node connection
            zfo (bool): zfo flag for swap
            token0 (Token): token0 of the pool
            token1 (Token): token1 of the pool
            fees (float): fees in pool
        """
        # constant contract address for UniswapV3 quoter
        # https://etherscan.io/address/0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6
        self._contract = node.eth.contract(address=self.ADDRESS, abi=self.ABI)
        self._zfo = zfo
        self._token0 = token0
        self._token1 = token1
        self._fees = fees

    def get_amount_out(self, amount_in: float) -> float:
        """
        Get amount out for given amount in

        Args:
            amount_in (float): amount in of the swap

        Returns:
            float: amount out of the swap
        """
        amount_in_decimals = int(amount_in * (10 ** self._token0.decimals if self._zfo else 10 ** self._token1.decimals))
        amount_out = self._contract.functions.quoteExactInputSingle(
            self._token0.address if self._zfo else self._token1.address,
            self._token1.address if self._zfo else self._token0.address,
            int(self._fees * 1_000_000),
            amount_in_decimals,
            0,
        ).call()
        return amount_out / (10 ** self._token1.decimals if self._zfo else 10 ** self._token0.decimals)
