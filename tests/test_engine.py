from typing import List

import pytest
from web3 import Web3

from service.creds import HTTP_NODE
from service.engine.swap_router import SwapRouter
from service.enums import DEX, Notional
from service.models import Pool, Token, Trade
from service.mongo import ORM


class MockedORM(ORM):

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database: str):
        self._database = database

    def get_all_pools_by_symbol(self, symbol: str) -> List[Pool]:

        return [
            Pool(
                address='0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852',
                dex=DEX.UNISWAP_V2,
                zfo=False,
                fees=0.003,
                notional=Notional.WETH,
                token0=Token(
                        address='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                        decimals=18,
                        symbol='WETH',
                    ),
                token1=Token(
                        address='0xdAC17F958D2ee523a2206206994597C13D831ec7',
                        decimals=6,
                        symbol='USDT',
                    ),
            ),
            Pool(
                address='0x11b815efB8f581194ae79006d24E0d814B7697F6',
                dex=DEX.UNISWAP_V3,
                zfo=False,
                fees=0.0005,
                notional=Notional.WETH,
                token0=Token(
                        address='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                        decimals=18,
                        symbol='WETH',
                    ),
                token1=Token(
                        address='0xdAC17F958D2ee523a2206206994597C13D831ec7',
                        decimals=6,
                        symbol='USDT',
                    ),
            ),
            Pool(
                address='0x3041CbD36888bECc7bbCBc0045E3B1f144466f5f',
                dex=DEX.UNISWAP_V2,
                zfo=False,
                fees=0.003,
                notional=Notional.USDC,
                token0=Token(
                        address='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                        decimals=6,
                        symbol='USDC',
                    ),
                token1=Token(
                        address='0xdAC17F958D2ee523a2206206994597C13D831ec7',
                        decimals=6,
                        symbol='USDT',
                    ),
            ),
            Pool(
                address='0x7858E59e0C01EA06Df3aF3D20aC7B0003275D4Bf',
                dex=DEX.UNISWAP_V3,
                zfo=False,
                fees=0.0005,
                notional=Notional.USDC,
                token0=Token(
                        address='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                        decimals=6,
                        symbol='USDC',
                    ),
                token1=Token(
                        address='0xdAC17F958D2ee523a2206206994597C13D831ec7',
                        decimals=6,
                        symbol='USDT',
                    ),
            ),
        ]


@pytest.fixture
def big_size_router():
    orm = MockedORM()
    node = Web3(Web3.HTTPProvider(HTTP_NODE))
    return SwapRouter(
        trade=Trade(amount=10_000_000, token_in_symbol='USDT'),
        mongo_orm=orm, node=node
    )


@pytest.fixture
def low_size_router():
    orm = MockedORM()
    node = Web3(Web3.HTTPProvider(HTTP_NODE))
    return SwapRouter(trade=Trade(amount=1_000, token_in_symbol='USDT'), mongo_orm=orm, node=node)


def test_big_size_usdt(big_size_router):
    assert big_size_router.find_pool().address == '0x7858E59e0C01EA06Df3aF3D20aC7B0003275D4Bf'


def test_low_size_usdt(low_size_router):
    assert low_size_router.find_pool().address == '0x7858E59e0C01EA06Df3aF3D20aC7B0003275D4Bf'
