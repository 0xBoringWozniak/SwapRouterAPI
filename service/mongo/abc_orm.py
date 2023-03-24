from abc import ABC, abstractmethod
from typing import List

from service.models import Pool


class ORM(ABC):
    """
    ORM Interface.
    """
    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database: str):
        self._database = database

    @abstractmethod
    def get_all_pools_by_symbol(self, symbol: str) -> List[Pool]:
        """
        Get all pools by symbol. Symbol is used to get collection name.
        Example: symbol = 'USDT' -> collection = 'usdt_pools'
        """
        raise NotImplementedError
