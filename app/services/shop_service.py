from fastapi import HTTPException, status
from app.models.shop import ShopRegister
from app.models.shop_contact import ShopContactRegister
from app.models.shop_schedule import ShopRegisterSchedule
from app.repositories import shop_repository as shop_repo
from app.repositories import shop_contact_repository as contact_repo
from app.repositories import shop_schedule_repository as sche_repo

import asyncpg
import asyncio

async def register_shop(pool: asyncpg.pool, data: ShopRegister, dueno_id: int, rol: str):
    if rol != "negocio":
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Solo los usuarios tipo negocio pueden registrar un negocio."
        )
        
    shop = await shop_repo.create_shop(
        pool,
        id_owner = dueno_id,
        name = data.nombre,
        description = data.descripcion,
        category = data.categoria_negocio,
        shop_img = data.imagen_negocio,
    )
    
    return shop

async def get_my_shops(pool: asyncpg.Pool, owner_id: int):
    shops = await shop_repo.get_shops_by_owner(pool, owner_id)
    return shops

async def get_shop_by_id(pool: asyncpg.Pool, shop_id: int, current_user_id: int):
    shop = await shop_repo.get_shop_by_id(pool, shop_id)
    if not shop:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Negocio no encontrado.")
    
    if shop["dueno_id"] != current_user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No tienes permiso para ver este negocio.")
    
    return shop

async def get_shop_full_profile(pool: asyncpg.Pool, shop_id: int):
    shop = await shop_repo.get_shop_by_id(pool, shop_id)
    
    if not shop:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Negocio no encontrado.")
    
    contacts = await get_contacts_by_shop(pool, shop_id)
    schedule = await get_weekly_schedule(pool, shop_id)
    
    return{
        "general": dict(shop),
        "contacto": [dict(c) for c in contacts],
        "horario" : [dict(sh) for sh in schedule],
    }

# SERVICES FOR CONTACT
async def add_contact(pool: asyncpg.Pool, shop_id: int, data: ShopContactRegister,
                      current_user_id: int):
    shop = await shop_repo.get_shop_by_id(pool, shop_id)
    
    if not shop:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Negocio no encontrado.")
    
    if shop['dueno_id'] != current_user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No tienes permiso para editar este negocio")
    
    exist_contact = await contact_repo.get_contact_by_shop_and_red(
        pool, shop_id, data.nombre_red.value
    )
    
    if exist_contact:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Ya existe un contacto de tipo '{data.nombre_red.value}' para este negocio"
        )
    
    contact = await contact_repo.create_contact(
        pool, shop_id, data.nombre_red.value, data.url
    )
    
    return contact

async def get_contacts_by_shop(pool: asyncpg.Pool, shop_id: int):
    conatcts = await contact_repo.get_contact_by_shop(pool, shop_id)
    return conatcts

#SERVICE FOR ADDRESS

#SERVICE FOR SCHEDULE

async def get_weekly_schedule(pool: asyncpg.Pool, shop_id: int):
    schedule = await sche_repo.get_weekly_schedule(pool, shop_id)
    return schedule

async def insert_schedule(
    pool: asyncpg.Pool, shop_id: int, data: ShopRegisterSchedule, current_user_id:int
    ):
    shop = await shop_repo.get_shop_by_id(pool, shop_id)
    
    if not shop:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Negocio no encontrado.")
            
    if shop["dueno_id"] != current_user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No tienes permiso para ver este negocio.")
    
    exist_day = await sche_repo.get_day_by_shop_and_day(pool, shop_id, data.dia)
    
    if exist_day:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"""
                Ya existe el dia {data.dia} registrado. Si quiere modificarlo elija la opción 
                'Editar'
            """
        )
    
    schedule = await sche_repo.create_schedule(
        pool, shop_id, data.dia, data.hora_apertura, data.hora_cierre
    )
    
    return schedule