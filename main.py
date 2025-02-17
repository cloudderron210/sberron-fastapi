from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse 
from core.helpers import CustomValidationError
from api_v1 import router as router_v1
from contextlib import asynccontextmanager
from core.config import settings





    
app = FastAPI()
        
@app.exception_handler(CustomValidationError)
async def custom_validation_exeption_handler(request: Request, exc: CustomValidationError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": [
                {
                    "type": exc.type,
                    "loc": exc.loc,
                    "msg": exc.detail,
                    "input": exc.input
                }
            ]
        }
    )

app.include_router(router_v1, prefix=settings.apiv1_prefix)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
