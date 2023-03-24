from service.models import Pool, Token
from service.creds import MONGO_URI
from service.mongo import MongoORM


orm = MongoORM(mongo_uri=MONGO_URI)
orm.database = 'dataprod'


pools = [
            Pool(
                address='0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852',
                dex='uniswap_v2',
                zfo=False,
                fees=0.003,
                notional='weth',
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
                dex='uniswap_v3',
                zfo=False,
                fees=0.0005,
                notional='weth',
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
                dex='uniswap_v2',
                zfo=False,
                fees=0.003,
                notional='usdc',
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
                dex='uniswap_v3',
                zfo=False,
                fees=0.0005,
                notional='usdc',
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


if __name__ == '__main__':
    orm.add_pools('usdt', pools)
