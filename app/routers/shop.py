from fastapi import APIRouter, Depends
from app.core.dependencies import get_db_pool, verify_api_key, get_current_user
from app.models.shop import ShopRegister, ShopOut
from app.services import shop_service

import asyncpg

router = APIRouter(prefix="/shop", tags=["shop"], dependencies=[Depends(verify_api_key)])

@router.post('/register-shop', response_model=ShopOut, status_code=201)
async def register_shop(
    data: ShopRegister,
    current_user : dict = Depends(get_current_user),
    pool: asyncpg.Pool = Depends(get_db_pool),
    ):
    
    shop = await shop_service.register_shop(
        pool,
        data,
        dueno_id = int(current_user['sub']),
        rol = current_user['rol'],
    )
    
    return dict(shop)