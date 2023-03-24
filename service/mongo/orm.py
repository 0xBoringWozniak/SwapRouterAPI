from typing import Dict, List

from bson import BSON
from pymongo import MongoClient

from service.models import Pool
from service.mongo.abc_orm import ORM
from service.mongo.codecs import codec_options
from service.mongo.exceptions import EmptyDataBaseException


class MongoORM(ORM):
    """
    Mongo ORM.
    """

    def __init__(self, mongo_uri: str) -> None:
        """
        Init Mongo ORM.

        Args:
            mongo_uri (str): mongo uri in format mongodb://<user>:<password>@<host>:<port>
                             should be passed from env variable from creds.py
        """
        self._client: MongoClient = MongoClient(mongo_uri)
        self._database: str = None

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database: str):
        self._database = database

    def __check_databse(self) -> None:
        """Check if database is set.

        Raises:
            EmptyDataBaseException: if database is not set
        """
        if self._database is None:
            raise EmptyDataBaseException('Database is not set')

    def get_all_pools_by_symbol(self, symbol: str) -> List[Pool]:
        """
        Get all pools by symbol. Symbol is used to get collection name.
        Example: symbol = 'USDT' -> collection = 'usdt_pools'

        Args:
            symbol (str): symbol of the token

        Returns:
            List[Pool]: list of pools for given symbol
        """
        self.__check_databse()
        collection = self._client[self._database][f'{symbol.lower()}_pools']
        pools = collection.find({})
        return [Pool(**pool) for pool in pools]

    def add_pool(self, symbol: str, pool: Pool) -> None:
        """
        Add pool to database. Pool object is converted to dict and then to bson.
        Args:
            symbol (str): symbol of the token
            pool (Pool): pool object
        """
        self.__check_databse()
        collection = self._client[self._database][f'{symbol.lower()}_pools']
        encoded_dict: Dict = BSON.decode(BSON.encode(pool.dict(), codec_options=codec_options))
        collection.insert_one(encoded_dict)

    def add_pools(self, symbol: str, pools: List[Pool]) -> None:
        """
        Add pools to database. Pool object is converted to dict and then to bson.

        Args:
            symbol (str): symbol of the token
            pools (List[Pool]): list of pools
        """
        for pool in pools:
            self.add_pool(symbol=symbol, pool=pool)
