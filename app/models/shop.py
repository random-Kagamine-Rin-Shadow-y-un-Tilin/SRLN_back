from pydantic import BaseModel
from typing import Optional
from datetime import time

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
    
class ShopScheduleOut(BaseModel):
    id_horario: int
    dia: str
    hora_apertura: time
    hora_cierre : time

class ShopFullProfileOut(BaseModel):
    general: ShopOut
    contacto: list[ShopContactOut] = []
    horario: list[ShopScheduleOut] = []