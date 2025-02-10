from fastapi import APIRouter

from api_v1.client.views import router as client_router
from api_v1.account.views import router as account_router
from api_v1.funds.views import router as funds_router


router = APIRouter()
router.include_router(client_router, prefix='/client')
router.include_router(account_router, prefix='/account')
router.include_router(funds_router, prefix='/funds')
