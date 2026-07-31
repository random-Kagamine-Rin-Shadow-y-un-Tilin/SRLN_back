import asyncpg

async def create_shop(pool: asyncpg.Pool, id_owner: int, name: str, description: str,
                      category: str, shop_img: str = None):
    query = """
        INSERT INTO negocios (dueno_id, nombre, descripcion, fecha_creacion, imagen_negocio,
        categoria_negocio) VALUES($1, $2, $3, now(), $4, $5)
        RETURNING id, nombre, descripcion, imagen_negocio, categoria_negocio
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, id_owner, name, description, shop_img, category)
    
async def get_shops_by_owner(pool: asyncpg.Pool, id_owner: int):
    query = """
        SELECT id, nombre, descripcion, categoria_negocio, imagen_negocio
        FROM negocios
        WHERE dueno_id = $1
        ORDER BY fecha_creacion DESC
    """
    
    async with pool.acquire() as conn:
        return await conn.fetch(query, id_owner)
    