import os

import pytest

from web3 import Web3

from helpers.init_pools import ASSETS
from helpers.abis import ERC_20_ABI

@pytest.fixture
def w3():
    return Web3(Web3.HTTPProvider(os.getenv('HTTP_NODE')))

@pytest.mark.parametrize("asset", ASSETS)
def test_assets(asset, w3):
    addresss = Web3.to_checksum_address(ASSETS[asset])
    token_contract = w3.eth.contract(address=addresss, abi=ERC_20_ABI)
    symbol_contract = token_contract.functions.symbol().call()
    assert asset == symbol_contract or 'W'+asset == symbol_contract
