import asyncpg

async def get_all_shops(pool: asyncpg.Pool):
    query = """
        SELECT id, nombre, descripcion, imagen_negocio, categoria_negocio 
        FROM negocios where estado_negocio = true
    """
    async with pool.acquire() as conn:
        return await conn.fetch(query)


async def search_shop(pool: asyncpg.Pool, name: str):
    query = """
        SELECT id, nombre, descripcion, imagen_negocio, categoria_negocio 
        FROM negocios 
        WHERE nombre = $1 AND estado_negocio = true
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, name)
