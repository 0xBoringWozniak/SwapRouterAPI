from typing import Tuple

from web3 import Web3

from service.engine.contracts.abis import CURVE_ABI
from service.engine.contracts.connector import Connector
from service.models import Token


class CurveConnector(Connector):

    ABI = CURVE_ABI

    def __init__(
                self,
                node: Web3,
                address: str,
                zfo: int,
                token0: Token,
                token1: Token,
                fees: float,
            ) -> None:
        """
        Curve connector.

        Args:
            node (Web3): node connection
            address (str): address of the pool
            zfo (bool): zfo flag for swap
            token0 (Token): token0 of the pool
            token1 (Token): token1 of the pool
            fees (float): fees in pool
        """
        self._contract = node.eth.contract(address=address, abi=self.ABI)  # type: ignore
        self._zfo = zfo
        self._token0 = token0
        self._token1 = token1
        self._fees = fees

    def __get_indexes_for_trades(self) -> Tuple[int, int]:
        """
        Get indexes for trades from zfo.

        Returns:
            Tuple[int, int]: indexes for trades
        """
        i, j = self._zfo // 10, self._zfo % 10
        return i, j

    def get_amount_out(self, amount_in: float) -> float:
        """
        Get amount out for given amount in.
        get_dy_underlying is used for getting amount out.

        Args:
            amount_in (float): amount in of the swap

        Returns:
            float: amount out of the swap
        """
        i, j = self.__get_indexes_for_trades()
        amount_out = self._contract.functions.get_dy_underlying(
            i, j, int(amount_in * (10 ** self._token0.decimals))).call()
        return amount_out / 10 ** self._token1.decimals
