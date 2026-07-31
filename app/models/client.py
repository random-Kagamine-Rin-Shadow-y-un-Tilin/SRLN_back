from pydantic import BaseModel

class ShopView(BaseModel):
    id: int
    nombre: str
    descripcion: str
    imagen_negocio: str
    categoria_negocio: str