from service.creds import MONGO_URI
from service.enums import DEX, Notional
from service.models import Pool, Token
from service.mongo import MongoORM

orm = MongoORM(mongo_uri=MONGO_URI)
orm.database = 'dataprod'


usdt_pools = [
            Pool(
                address='0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852',
                dex=DEX.UNISWAP_V2,
                zfo=0,
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
                zfo=0,
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
                zfo=0,
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
                zfo=0,
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
            Pool(
                address='0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7',
                dex=DEX.CURVE,
                zfo=21,
                fees=0.01,
                notional=Notional.USDC,
                token0=Token(
                        address='0xdAC17F958D2ee523a2206206994597C13D831ec7',
                        decimals=6,
                        symbol='USDT',
                    ),
                token1=Token(
                        address='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                        decimals=6,
                        symbol='USDC',
                    ),
            ),
        ]


if __name__ == '__main__':
    orm.add_pools('usdt', usdt_pools)
