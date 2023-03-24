from typing import Tuple

from fastapi import APIRouter, FastAPI
from web3 import Web3

from service.api.exceptions import SwapRouterLogicError, SymbolError
from service.creds import HTTP_NODE, MONGO_URI
from service.engine import SwapRouter
from service.log import app_logger
from service.models import Pool, Trade
from service.mongo import MongoORM

router = APIRouter()


def build_connections() -> Tuple[MongoORM, Web3]:
    mongo_orm = MongoORM(mongo_uri=MONGO_URI)
    mongo_orm.database = 'dataprod'
    node = Web3(Web3.HTTPProvider(HTTP_NODE))
    return mongo_orm, node


MONGO_ORM, NODE = build_connections()


@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    """
    Health service check.
    """
    return "I am alive"


@router.post(
    path="/find_pool",
    tags=["Find Pool"],
    response_model=Pool,
)
async def find_pool(trade: Trade) -> Pool:
    """
    Find a pool for a given trade.
    """
    pools = MONGO_ORM.get_all_pools_by_symbol(trade.token_in_symbol)
    app_logger.info("Found %s pools for %s", len(pools), trade.token_in_symbol)
    if not pools:
        raise SymbolError(error_loc=trade.token_in_symbol)
    try:
        swap_router = SwapRouter(trade=trade, mongo_orm=MONGO_ORM, node=NODE)
        return swap_router.find_pool()
    except Exception as e:
        raise SwapRouterLogicError(error_message=str(e)) from e


def add_views(app: FastAPI) -> None:
    app.include_router(router)
