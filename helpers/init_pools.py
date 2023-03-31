import pickle
import os
from typing import Dict, List

from web3 import Web3

from service.models import Pool

from helpers.preprocess_pools import (
    get_uniswap_v2_pool_usdc, get_uniswap_v2_pool_weth,
    get_uniswap_v3_pool_usdc, get_uniswap_v3_pool_weth,
    get_curve_pool
)
from helpers.abis import UNISWAP_V2_FACTORY_ABI, UNISWAP_V3_FACTORY_ABI


w3 = Web3(Web3.HTTPProvider(os.getenv('HTTP_NODE')))

univ2_factory = w3.eth.contract(address='0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f', abi=UNISWAP_V2_FACTORY_ABI)
univ3_factory = w3.eth.contract(address='0x1F98431c8aD98523631AE4a59f267346ea31F984', abi=UNISWAP_V3_FACTORY_ABI)

# target assets
USDC = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
WETH = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

# assets to find pools for
ASSETS = {
    '1INCH': '0x111111111117dC0aa78b770fA6A738034120C302',
    'AAVE': '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9',
    'USDT': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    'BTC': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
    'YFI': '0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e',
    'ZRX': '0xE41d2489571d322189246DaFA5ebDe1F4699F498',
    'LINK': '0x514910771AF9Ca656af840dff83E8264EcF986CA',
    'SNX': '0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F',
    'UNI': '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984',
    'COMP': '0xc00e94Cb662C3520282E6f5717214004A7f26888',
    # 'MKR': '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2', # MKR has bytes32 symbol
    'SUSHI': '0x6B3595068778DD592e39A122f4f5a5cF09C90fE2',
    'BAL': '0xba100000625a3754423978a60c9317c58a424e3D',
    'BAT': '0x0D8775F648430679A709E98d2b0Cb6250d2887EF',
    'BUSD': '0x4Fabb145d64652a948d72533023f6E7A623C7C53',
    'DAI': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
    'ENJ': '0xF629cBd94d3791C9250152BD8dfBDF380E2a3B9c',
    'KNC': '0xdd974D5C2e2928deA5F71b9825b8b646686BD200',
    'MANA': '0x0F5D2fB29fb7d3CFeE444a200298f468908cC942',
    'sUSD': '0x57Ab1ec28D129707052df4dF418D58a2D46d5f51',
    'TUSD': '0x0000000000085d4780B73119b644AE5ecd22b376',
    'REN': '0x408e41876cCCDC0F92210600ef50372656052a38',
    'LUSD': '0x5f98805A4E8be255a32880FDeC7F6728C6568bA0',
    'CRV': '0xD533a949740bb3306d119CC777fa900bA034cd52',
    'GUSD': '0x056Fd409E1d7A124BD7017459dFEa2F387b6d5Cd',
    'USDP': '0x1456688345527bE1f37E9e627DA0837D6f08C925',
    'RAI': '0x03ab458634910AaD20eF5f1C8ee96F1D6ac54919',
    'AMPL': '0xd46ba6d942050d489dbd938a2c909a5d5039a161',
    'DPI': '0x1494CA1F11D487c2bBe4543E90080AeBa4BA3C2b',
    'FRAX': '0x853d955aCEf822Db058eb8505911ED77F175b99e',
    'FEI': '0x956F47F50A910163D8BF957Cf5846D573E7f87CA',
    'stETH': '0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84',
    'CVX': '0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B',
}

CURVE_POOLS = {
    'DAI': '0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7',
    'USDT': '0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7',
    'BUSD': '0x4807862AA8b2bF68830e4C8dc86D0e9A998e085a',
    'FRAX': '0xDcEF968d416a41Cdac0ED8702fAC8128A64241A2',
    'GUSD': '0x4f062658eaaf2c1ccf8c8e36d6824cdf41167956',
    'LUSD': '0xEd279fDD11cA84bEef15AF5D39BB4d4bEE23F0cA',
    # 'sUSD': '0xA5407eAE9Ba41422680e2e00537571bcC53efBfD', # sUSD has int128 coins signature
    'TUSD': '0xecd5e75afb02efa118af914515d6521aabd189f1',
    'PUSD': '0xc270b3B858c335B6BA5D5b10e2Da8a09976005ad',
}

if __name__ == '__main__':

    pools: Dict[str, List[Pool]] = {}
    for asset, address in ASSETS.items():
        print(f'Processing {asset}')
        address = Web3.to_checksum_address(address)
        univ2_pair_usdc = univ2_factory.functions.getPair(address, USDC).call()
        print(f'Univ2 pair USDC: {univ2_pair_usdc}')
        univ2_pair_weth = univ2_factory.functions.getPair(address, WETH).call()
        print(f'Univ2 pair WETH: {univ2_pair_weth}')
        univ3_pair_usdc_03 = univ3_factory.functions.getPool(address, USDC, 3000).call()
        print(f'Univ3 pair USDC 0.3%: {univ3_pair_usdc_03}')
        univ3_pair_usdc_005 = univ3_factory.functions.getPool(address, USDC, 500).call()
        print(f'Univ3 pair USDC 0.05%: {univ3_pair_usdc_005}')
        univ3_pair_usdc_01 = univ3_factory.functions.getPool(address, USDC, 10000).call()
        print(f'Univ3 pair USDC 0.1%: {univ3_pair_usdc_01}')
        univ3_pair_weth_03 = univ3_factory.functions.getPool(address, WETH, 3000).call()
        print(f'Univ3 pair WETH 0.3%: {univ3_pair_weth_03}')
        univ3_pair_weth_005 = univ3_factory.functions.getPool(address, WETH, 500).call()
        print(f'Univ3 pair WETH 0.05%: {univ3_pair_weth_005}')
        univ3_pair_weth_01 = univ3_factory.functions.getPool(address, WETH, 10000).call()
        print(f'Univ3 pair WETH 0.1%: {univ3_pair_weth_01}')
    
        pools[asset] = []
        if univ2_pair_usdc != ZERO_ADDRESS:
            pools[asset].append(get_uniswap_v2_pool_usdc(univ2_pair_usdc))
        if univ2_pair_weth != ZERO_ADDRESS:
            pools[asset].append(get_uniswap_v2_pool_weth(univ2_pair_weth))
        if univ3_pair_usdc_03 != ZERO_ADDRESS:
            pools[asset].append(get_uniswap_v3_pool_usdc(univ3_pair_usdc_03))
        if univ3_pair_usdc_005 != ZERO_ADDRESS:
            pools[asset].append(get_uniswap_v3_pool_usdc(univ3_pair_usdc_005))
        if univ3_pair_usdc_01 != ZERO_ADDRESS:
            pools[asset].append(get_uniswap_v3_pool_usdc(univ3_pair_usdc_01))
        if univ3_pair_weth_03 != ZERO_ADDRESS:
            pools[asset].append(get_uniswap_v3_pool_weth(univ3_pair_weth_03))
        if univ3_pair_weth_005 != ZERO_ADDRESS:
            pools[asset].append(get_uniswap_v3_pool_weth(univ3_pair_weth_005))
        if univ3_pair_weth_01 != ZERO_ADDRESS:
            pools[asset].append(get_uniswap_v3_pool_weth(univ3_pair_weth_01))

        if asset in CURVE_POOLS:
            pools[asset].append(get_curve_pool(asset, CURVE_POOLS[asset]))

        print(f'Finished {asset}: {len(pools[asset])} pools')

    with open('pools.json', 'wb+') as file:
        pickle.dump(pools, file)
