import os
from typing import List

from fastapi import APIRouter, Depends, FastAPI, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.api_key import APIKey, APIKeyHeader, APIKeyQuery
from pydantic import BaseModel

from service.api.exceptions import (
    AuthorizationError
)
from service.log import app_logger


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


router = APIRouter()

@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    return "I am alive"


def add_views(app: FastAPI) -> None:
    app.include_router(router)
