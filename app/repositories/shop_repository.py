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
    