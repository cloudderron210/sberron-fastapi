from fastapi import APIRouter

from api_v1.users.views import router as client_router
from api_v1.account.views import router as account_router
from api_v1.funds.views import router as funds_router
from api_v1.currencies.views import router as currencies_router


router = APIRouter()
router.include_router(client_router, prefix='/user')
router.include_router(account_router, prefix='/account')
router.include_router(funds_router, prefix='/funds')
router.include_router(currencies_router, prefix='/currency')
