from fastapi import HTTPException, status
from app.models.shop import ShopRegister
from app.repositories import shop_repository as repo

import asyncpg

async def register_shop(pool: asyncpg.pool, data: ShopRegister, dueno_id: int, rol: str):
    if rol != "negocio":
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Solo los usuarios tipo negocio pueden registrar un negocio."
        )
        
    shop = await repo.create_shop(
        pool,
        id_owner = dueno_id,
        name = data.nombre,
        description = data.descripcion,
        category = data.categoria_negocio,
        shop_img = data.imagen_negocio,
    )
    
    return shop

async def get_my_shops(pool: asyncpg.Pool, owner_id: int):
    shops = await repo.get_shops_by_owner(pool, owner_id)
    return shops