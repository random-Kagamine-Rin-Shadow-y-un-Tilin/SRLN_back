# app/routers/perfil.py
from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["perfil"])

@router.get("/me")
async def my_profile(current_user: dict = Depends(get_current_user)):
    print(current_user)
    return {"id": current_user['sub'], "rol": current_user['rol'], "nombre": current_user['nombre']}