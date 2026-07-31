from fastapi import HTTPException, status
from app.models.client import ShopView
from app.repositories import client_repository as repo
from typing import Optional, List
import asyncpg

# Listado normal
async def list_shops(pool: asyncpg.Pool):
    shops = await repo.get_all_shops(pool)
    if not shops:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay negocios registrados"
        )
    return [dict(shop) for shop in shops]

#Listado con filtro de nombre
async def search_shops_by_name(pool: asyncpg.Pool, search_term: str):
    if not search_term or len(search_term.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El término de búsqueda debe tener al menos 2 caracteres"
        )
    
    shops = await repo.search_shops_by_name(pool, search_term.strip())
    if not shops:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron negocios con '{search_term}'"
        )
    return [dict(shop) for shop in shops]

#Listado con filtro de categoria
async def search_shops_by_category(pool: asyncpg.Pool, category: str):
    if not category or len(category.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría debe tener al menos 2 caracteres"
        )
    
    shops = await repo.search_shops_by_category(pool, category.strip())
    if not shops:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron negocios en la categoría '{category}'"
        )
    return [dict(shop) for shop in shops]

#Listado con filtro de nombre o categoria
async def search_shops(pool: asyncpg.Pool, search_term: str):
    if not search_term or len(search_term.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El término de búsqueda debe tener al menos 2 caracteres"
        )
    
    shops = await repo.search_shops(pool, search_term.strip())
    if not shops:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron negocios relacionados con '{search_term}'"
        )
    return [dict(shop) for shop in shops]
