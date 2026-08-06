from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from app.core.dependencies import get_db_pool, verify_api_key, get_current_user
from app.models.shop import ShopRegister, ShopOut, ShopFullProfileOut
from app.models.shop_contact import ShopContactRegister, ShopContactOut
from app.services import shop_service
from app.core.storage import upload_img

import asyncpg

router = APIRouter(prefix="/shop", tags=["shop"], dependencies=[Depends(verify_api_key)])

@router.post('/register-shop', response_model=ShopOut, status_code=201)
async def register_shop(
    data: ShopRegister,
    current_user : dict = Depends(get_current_user),
    pool: asyncpg.Pool = Depends(get_db_pool),
    ):
    
    shop = await shop_service.register_shop(
        pool,
        data,
        dueno_id = int(current_user['sub']),
        rol = current_user['rol'],
    )
    
    return dict(shop)

@router.post("/upload-image")
async def submit_img(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    if current_user["rol"] != "negocio":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo negocios pueden subir imagenes.")
    
    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Formato de imagen no permitido.")
    
    content = await file.read()
    
    if len(content) > 5 * 1024 * 1024: #Max 5mb
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "La imagen no debe superar 5MB.")
    
    
    url = await upload_img(content, file.filename, file.content_type)
    return {"url": url}

@router.get("/my-shops", response_model=list[ShopOut])
async def get_my_shops(
    current_user : dict = Depends(get_current_user),
    pool: asyncpg.Pool = Depends(get_db_pool)
):
    shops = await shop_service.get_my_shops(pool, int(current_user["sub"]))
    return [dict(shop) for shop in shops]

@router.get("/get-shop/{shop_id}", response_model=ShopFullProfileOut)
async def get_shop_by_id(
    shop_id: int,
    pool: asyncpg.Pool = Depends(get_db_pool)
):
    return await shop_service.get_shop_full_profile(pool, shop_id)

#Contact routes

@router.post("/register-contact/{shop_id}", response_model=ShopContactOut, status_code=201)
async def add_contact(
    shop_id: int,
    data: ShopContactRegister,
    current_user : dict = Depends(get_current_user),
    pool: asyncpg.Pool = Depends(get_db_pool)
):
    contact = await shop_service.add_contact(pool, shop_id, data, int(current_user["sub"]))
    return dict(contact)