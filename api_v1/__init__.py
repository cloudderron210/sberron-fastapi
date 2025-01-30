from fastapi import APIRouter

from api_v1.client.views import router as client_router


router = APIRouter()
router.include_router(client_router, prefix='/client')
