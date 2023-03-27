from web3 import Web3

from service.engine.contracts.connector import Connector
from service.engine.contracts.curve import CurveConnector
from service.engine.contracts.uniswap_v2 import UniswapV2Connector
from service.engine.contracts.uniswap_v3 import UniswapV3Connector
from service.enums import DEX
from service.models import Pool


class DEXConnectorRouter:
    """
    DEX Connector Router.
    Returns connector for given dex through get_connector.
    Raises:
        NotImplementedError: if dex is not supported
    """

    @classmethod
    def get_connector(cls, node: Web3, pool: Pool) -> Connector:
        """
        Get connector for given dex.
        Connector is resolvable by dex filed.

        Args:
            node (Web3.HTTPProvider): node connection
            pool (Pool): pool model

        Raises:
            NotImplementedError: if dex is not supported

        Returns:
            Connector: connector for given dex

        Now we have only Uniswap V2 and Uniswap V3 connectors.
        TODO: add more connectors for other dexes:
            - Curve
            - Balancer
        """
        if pool.dex == DEX.UNISWAP_V2:
            return UniswapV2Connector(
                node=node, zfo=pool.zfo,
                fees=pool.fees, token0=pool.token0, token1=pool.token1
            )
        if pool.dex == DEX.UNISWAP_V3:
            return UniswapV3Connector(
                node=node, zfo=pool.zfo,
                fees=pool.fees, token0=pool.token0, token1=pool.token1
            )
        if pool.dex == DEX.CURVE:
            return CurveConnector(
                node=node, address=pool.address, zfo=pool.zfo,
                fees=pool.fees, token0=pool.token0, token1=pool.token1
            )
        raise NotImplementedError
