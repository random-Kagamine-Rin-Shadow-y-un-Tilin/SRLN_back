from pydantic import BaseModel

class ShopRegister(BaseModel):
    nombre: str
    descripcion: str
    imagen_negocio: str
    categoria_negocio: str
    
class ShopOut(BaseModel):
    id: int
    nombre: str
    descripcion: str
    imagen_negocio: str
    categoria_negocio: str