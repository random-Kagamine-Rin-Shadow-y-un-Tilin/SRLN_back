import asyncpg
from typing import Optional, List

# Consulta de todos los negocios-------------------------------------------
async def get_all_shops(pool: asyncpg.Pool):
    query = """
        SELECT id, nombre, descripcion, imagen_negocio, categoria_negocio 
        FROM negocios where estado_negocio = true
    """
    async with pool.acquire() as conn:
        return await conn.fetch(query)

# Busqueda de negocio por nombre -------------------------------------------
async def search_shops_by_name(pool: asyncpg.Pool, search_term: str):
    query = """
        SELECT id, nombre, descripcion, imagen_negocio, categoria_negocio 
        FROM negocios 
        WHERE estado_negocio = true 
        AND LOWER(nombre) LIKE LOWER($1)
        ORDER BY nombre
    """
    async with pool.acquire() as conn:
        return await conn.fetch(query, f"%{search_term}%")

# Busqueda de negocio por categoria ----------------------------------------
async def search_shops_by_category(pool: asyncpg.Pool, category: str):
    query = """
        SELECT id, nombre, descripcion, imagen_negocio, categoria_negocio 
        FROM negocios 
        WHERE estado_negocio = true 
        AND LOWER(categoria_negocio) = LOWER($1)
        ORDER BY nombre
    """
    async with pool.acquire() as conn:
        return await conn.fetch(query, category)
    
#Busqueda de negocio por nombre y categoria --------------------------------
async def search_shops(pool: asyncpg.Pool, search_term: str):
    query = """
        SELECT id, nombre, descripcion, imagen_negocio, categoria_negocio 
        FROM negocios 
        WHERE estado_negocio = true 
        AND (
            LOWER(nombre) LIKE LOWER($1) 
            OR LOWER(descripcion) LIKE LOWER($1)
            OR LOWER(categoria_negocio) LIKE LOWER($1)
        )
        ORDER BY nombre
    """
    async with pool.acquire() as conn:
        return await conn.fetch(query, f"%{search_term}%")