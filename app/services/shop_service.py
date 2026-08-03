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

async def get_shop_by_id(pool: asyncpg.Pool, shop_id: int, current_user_id: int):
    shop = await repo.get_shop_by_id(pool, shop_id)
    if not shop:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Negocio no encontrado.")
    
    if shop["dueno_id"] != current_user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No tienes permiso para ver este negocio.")
    
    return shop