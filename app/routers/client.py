from fastapi import APIRouter, Depends, Query
from app.core.dependencies import get_db_pool, verify_api_key, get_current_user
from app.models.client import ShopView
from app.services import client_service
from typing import Optional, List

import asyncpg

router = APIRouter(prefix="/client", tags=["client"], dependencies=[Depends(verify_api_key)])

# Traer todos los negocios
@router.get('/list-shops', response_model=list[ShopView])
async def list_shops(
    pool: asyncpg.Pool = Depends(get_db_pool)
    ):
    
    shops = await client_service.list_shops(pool)
    return shops

# Buscador de negocios general
@router.get('/search', response_model=list[ShopView])
async def search_shops(
    q: str = Query(..., min_length=2, description="Término de búsqueda"),
    pool: asyncpg.Pool = Depends(get_db_pool)
):
    shops = await client_service.search_shops(pool, q)
    return shops

# Buscador de negocios por nombre
@router.get('/search-by-name', response_model=list[ShopView])
async def search_shops_by_name(
    name: str = Query(..., min_length=2, description="Nombre del negocio"),
    pool: asyncpg.Pool = Depends(get_db_pool)
):
    shops = await client_service.search_shops_by_name(pool, name)
    return shops


# Buscador de negocios por categoría
@router.get('/search-by-category', response_model=list[ShopView])
async def search_shops_by_category(
    category: str = Query(..., min_length=2, description="Categoría del negocio"),
    pool: asyncpg.Pool = Depends(get_db_pool)
):
    shops = await client_service.search_shops_by_category(pool, category)
    return shops