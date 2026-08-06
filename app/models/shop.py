from pydantic import BaseModel
from typing import Optional

class ShopRegister(BaseModel):
    nombre: str
    descripcion: str
    imagen_negocio: Optional[str] = 'null'
    categoria_negocio: int
    
class ShopOut(BaseModel):
    id: int
    nombre: str
    descripcion: str
    imagen_negocio: str
    categoria_negocio: str | int
    
class ShopContactOut(BaseModel):
    nombre_red: str
    url: str

class ShopFullProfileOut(BaseModel):
    general: ShopOut
    contacto: list[ShopContactOut] = []