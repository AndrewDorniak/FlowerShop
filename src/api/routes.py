from fastapi import APIRouter

from src.api.registration import router as registration
from src.api.login.endpoints import router as login
from src.api.shop.endpoints import router as shop_router


router = APIRouter()

router.include_router(registration, tags=['registration'])
router.include_router(login, tags=['login'])
router.include_router(shop_router, tags=['shop'])
