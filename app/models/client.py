from pydantic import BaseModel
from typing import Optional

class ShopView(BaseModel):
    id: int
    nombre: str
    descripcion: str
    imagen_negocio: str
    categoria_negocio: str
    
class ShopSearchParams(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    # servicios: Optional[str] = None