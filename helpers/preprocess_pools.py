import os
from typing import List, Dict
from pprint import pprint

from web3 import Web3

from service.enums import DEX, Notional
from service.models import Pool, Token

from helpers.abis import CURVE_ABI, ERC_20_ABI, UNISWAP_V2_POOL_ABI, UNISWAP_V3_POOL_ABI


USDC_ADDRESS = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
w3 = Web3(Web3.HTTPProvider(os.getenv('HTTP_NODE')))


def get_curve_pool(symbol: str, address: str) -> Pool:
    address = Web3.to_checksum_address(address)
    contract = w3.eth.contract(address=address, abi=CURVE_ABI)
    token_zfo, usdc_zfo = None, None
    fees = contract.functions.fee().call() / 1e9
    for i in range(4):
        try:
            token_address = contract.functions.coins(i).call()
            token = w3.eth.contract(address=token_address, abi=ERC_20_ABI)
            token_symbol = token.functions.symbol().call()
            if token_symbol.lower() == symbol.lower():
                token0 = Token(address=token_address, symbol=token_symbol, decimals=token.functions.decimals().call())
                token_zfo = i
            if token_symbol == 'USDC':
                token1 = Token(address=USDC_ADDRESS, symbol='USDC', decimals=6)
                usdc_zfo = i
        except Exception as e:
            continue
    
    if usdc_zfo is None:
        usdc_zfo = 1 # 3CRV
        token1 = Token(address=USDC_ADDRESS, symbol='USDC', decimals=6)

    return Pool(
        address=address,
        dex=DEX.CURVE,
        notional=Notional.USDC,
        zfo=int(str(token_zfo)+str(usdc_zfo)),
        fees=fees,
        token0=token0,
        token1=token1,
    )

def get_uniswap_v2_pool_weth(address: str) -> Pool:
    address = Web3.to_checksum_address(address)
    contract = w3.eth.contract(address=address, abi=UNISWAP_V2_POOL_ABI)
    token0_contract = w3.eth.contract(address=contract.functions.token0().call(), abi=ERC_20_ABI)
    token1_contract = w3.eth.contract(address=contract.functions.token1().call(), abi=ERC_20_ABI)
    token0 = Token(address=token0_contract.address, symbol=token0_contract.functions.symbol().call(), decimals=token0_contract.functions.decimals().call())
    token1 = Token(address=token1_contract.address, symbol=token1_contract.functions.symbol().call(), decimals=token1_contract.functions.decimals().call())
    if token0.symbol == 'WETH':
        zfo = 0
    else:
        zfo = 1

    return Pool(
        address=address,
        dex=DEX.UNISWAP_V2,
        notional=Notional.WETH,
        zfo=zfo,
        fees=0.003,
        token0=token0,
        token1=token1,
    )

def get_uniswap_v2_pool_usdc(address: str) -> Pool:
    address = Web3.to_checksum_address(address)
    contract = w3.eth.contract(address=address, abi=UNISWAP_V2_POOL_ABI)
    token0_contract = w3.eth.contract(address=contract.functions.token0().call(), abi=ERC_20_ABI)
    token1_contract = w3.eth.contract(address=contract.functions.token1().call(), abi=ERC_20_ABI)
    token0 = Token(address=token0_contract.address, symbol=token0_contract.functions.symbol().call(), decimals=token0_contract.functions.decimals().call())
    token1 = Token(address=token1_contract.address, symbol=token1_contract.functions.symbol().call(), decimals=token1_contract.functions.decimals().call())
    if token0.symbol == 'USDC':
        zfo = 0
    else:
        zfo = 1

    return Pool(
        address=address,
        dex=DEX.UNISWAP_V2,
        notional=Notional.USDC,
        zfo=zfo,
        fees=0.003,
        token0=token0,
        token1=token1,
    )

def get_uniswap_v3_pool_weth(address: str) -> Pool:
    address = Web3.to_checksum_address(address)
    contract = w3.eth.contract(address=address, abi=UNISWAP_V3_POOL_ABI)
    token0_contract = w3.eth.contract(address=contract.functions.token0().call(), abi=ERC_20_ABI)
    token1_contract = w3.eth.contract(address=contract.functions.token1().call(), abi=ERC_20_ABI)
    token0 = Token(address=token0_contract.address, symbol=token0_contract.functions.symbol().call(), decimals=token0_contract.functions.decimals().call())
    token1 = Token(address=token1_contract.address, symbol=token1_contract.functions.symbol().call(), decimals=token1_contract.functions.decimals().call())
    fees = contract.functions.fee().call() / 1e6
    if token0.symbol == 'WETH':
        zfo = 0
    else:
        zfo = 1

    return Pool(
        address=address,
        dex=DEX.UNISWAP_V3,
        notional=Notional.WETH,
        zfo=zfo,
        fees=fees,
        token0=token0,
        token1=token1,
    )

def get_uniswap_v3_pool_usdc(address: str) -> Pool:
    address = Web3.to_checksum_address(address)
    contract = w3.eth.contract(address=address, abi=UNISWAP_V3_POOL_ABI)
    token0_contract = w3.eth.contract(address=contract.functions.token0().call(), abi=ERC_20_ABI)
    token1_contract = w3.eth.contract(address=contract.functions.token1().call(), abi=ERC_20_ABI)
    token0 = Token(address=token0_contract.address, symbol=token0_contract.functions.symbol().call(), decimals=token0_contract.functions.decimals().call())
    token1 = Token(address=token1_contract.address, symbol=token1_contract.functions.symbol().call(), decimals=token1_contract.functions.decimals().call())
    fees = contract.functions.fee().call() / 1e6
    if token0.symbol == 'USDC':
        zfo = 0
    else:
        zfo = 1

    return Pool(
        address=address,
        dex=DEX.UNISWAP_V3,
        notional=Notional.USDC,
        zfo=zfo,
        fees=fees,
        token0=token0,
        token1=token1,
    )
