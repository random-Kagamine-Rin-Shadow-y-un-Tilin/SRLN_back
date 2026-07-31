from fastapi import APIRouter, Depends
from app.core.dependencies import get_db_pool, verify_api_key, get_current_user
from app.models.client import ShopView
from app.services import client_service

import asyncpg

router = APIRouter(prefix="/client", tags=["client"], dependencies=[Depends(verify_api_key)])

@router.get('/list-shops', response_model=list[ShopView])
async def list_shops(
    pool: asyncpg.Pool = Depends(get_db_pool)
    ):
    
    shops = await client_service.list_shops(pool)
    return shops