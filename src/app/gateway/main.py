from fastapi import FastAPI
from middleware.auth_middlleware import AuthMiddleware
from fastapi.routing import APIRouter

router = APIRouter()
app = FastAPI()




app.add_middleware(AuthMiddleware)

@router.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(router)