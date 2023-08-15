from fastapi import APIRouter

from app.api.endpoints import shorturl_router, user_router, my_router

main_router = APIRouter()
main_router.include_router(
    shorturl_router,
    prefix='/shorten',
    tags=['Shorten']
)
main_router.include_router(my_router)
main_router.include_router(user_router)
