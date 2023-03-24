from typing import Dict
from dataclasses import dataclass

from web3 import Web3

from service.models import Trade, Pool
from service.enums import Notional
from service.mongo import MongoORM
from service.utils import get_ethusd_price

from service.engine.contracts import Connector, DEXConnectorRouter


@dataclass
class TradeStats:
    """
    Trade stats.
    """
    amount_out: float
    amount_out_in_usd: float


class SwapRouter:
    """
    Swap Router class for the API engine.
    """
    def __init__(self, trade: Trade, mongo_orm: MongoORM, node: Web3.HTTPProvider) -> None:
        """
        Args:
            trade (Trade): trade object
        """
        self.trade = trade
        self.__init_orm(mongo_orm)
        self._node = node

    def __init_orm(self, mongo_orm: MongoORM) -> None:
        self._orm = mongo_orm
        self._orm.database = 'dataprod'
    
    def find_pool(self) -> Pool:
        """
        Find a pool for a given trade.
        """
        trades_stats: Dict = {}

        pools = self._orm.get_all_pools_by_symbol(self.trade.token_in_symbol)
        for pool in pools:
            trades_stats[pool] = self.get_trade_stats(pool=pool)

        # find dex with the highest token_out_in_usd
        best_one = max(trades_stats, key=lambda x: trades_stats[x].amount_out_in_usd)
        return best_one

    def get_trade_stats(self, pool: Pool) -> TradeStats:
        """
        Get trade stats for a given trade.
        """
        connector: Connector = DEXConnectorRouter.get_connector(node=self._node, pool=pool)
        amount_out = connector.get_amount_out(self.trade.amount)

        if pool.notional == Notional.WETH:
            amount_out_in_usd = amount_out * get_ethusd_price(amount_out)
        else:
            amount_out_in_usd = amount_out

        return TradeStats(
            amount_out=amount_out,
            amount_out_in_usd=amount_out_in_usd,
        )
