from web3 import Web3

from service.engine.contracts.abis import UNISWAP_V2_QUOTER_ABI
from service.engine.contracts.connector import Connector
from service.models import Token


class UniswapV2Connector(Connector):

    ABI = UNISWAP_V2_QUOTER_ABI
    ADDRESS = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'

    def __init__(
                self,
                node: Web3,
                zfo: int,
                token0: Token,
                token1: Token,
                fees: float,
            ) -> None:
        """
        Uniswap V2 connector.

        Args:
            node (Web3): node connection
            zfo (bool): zfo flag for swap
            token0 (Token): token0 of the pool
            token1 (Token): token1 of the pool
            fees (float): fees in pool
        """
        # constant contract address for UniswapV3 quoter
        # https://etherscan.io/address/0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D
        self._contract = node.eth.contract(address=self.ADDRESS, abi=self.ABI)  # type: ignore
        self._zfo = zfo
        self._token0 = token0
        self._token1 = token1
        self._fees = fees

    def get_amount_out(self, amount_in: float) -> float:
        """
        Get amount out for given amount in. Uses Uniswap V2 Quoter contract.
        getAmountsOut is used for getting amount out.

        Args:
            amount_in (float): amount in of the swap

        Returns:
            float: amount out of the swap
        """
        amount_out = self._contract.functions.getAmountsOut(
            int(
                amount_in *
                (10**self._token0.decimals if self._zfo else
                 10**self._token1.decimals)
            ),
            [self._token0.address, self._token1.address] if self._zfo else
            [self._token1.address, self._token0.address]
        ).call()[-1]
        return amount_out / (10**self._token1.decimals if self._zfo else
                             10**self._token0.decimals)
