from typing import Dict

from web3 import Web3

from service.engine.contracts import Connector, DEXConnectorRouter
from service.enums import Notional
from service.log import app_logger
from service.models import Pool, Trade, TradeStats
from service.mongo import ORM
from service.utils import get_ethusd_price


class SwapRouter:
    """
    Swap Router class for the API engine.
    """
    def __init__(
                self, trade: Trade,
                mongo_orm: ORM, node: Web3
            ) -> None:
        """
        Args:
            trade (Trade): trade object
        """
        self.trade = trade
        self.__init_orm(mongo_orm)
        self._node = node

    def __init_orm(self, mongo_orm: ORM) -> None:
        self._orm = mongo_orm
        self._orm.database = 'dataprod'

    def find_pool(self) -> Pool:
        """
        Find a pool for a given trade.
        """
        trades_stats: Dict[Pool, TradeStats] = self.get_all_trades_stats()
        # find dex with the highest token_out_in_usd
        # exclude pools from self.trade.excludes_dexes
        trades_stats = {k: v for k, v in trades_stats.items() if k.dex not in self.trade.excluded_dexes}
        best_one = max(trades_stats, key=lambda x: trades_stats[x].amount_out_in_usd)
        return best_one

    def get_all_trades_stats(self) -> Dict[Pool, TradeStats]:
        """
        Get all trades stats for a given trade.
        """
        trades_stats: Dict[Pool, TradeStats] = {}

        pools = self._orm.get_all_pools_by_symbol(self.trade.token_in_symbol)
        for pool in pools:
            try:
                trades_stats[pool] = self.get_trade_stats(pool=pool)
            # we want to catch all exceptions here to avoid breaking the whole process
            except Exception as e:  # pylint: disable=broad-except
                app_logger.error("Error while getting trade stats for %s: %s", pool, e)

        return trades_stats

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
