from fastapi import HTTPException, status
from app.models.client import ShopView
from app.repositories import client_repository as repo
import asyncpg

async def list_shops(pool: asyncpg.Pool):
    shops = await repo.get_all_shops(pool)
    if not shops:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay negocios registrados"
        )
    return [dict(shop) for shop in shops]