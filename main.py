from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse 
from core.helpers import CustomValidationError
from api_v1 import router as router_v1
from contextlib import asynccontextmanager
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware





    
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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
