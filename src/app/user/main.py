from fastapi import FastAPI
from fastapi.routing import APIRouter
from .config.config import AppConfig

from .apis.user_controller import router as user_router
from .database import engine, Base

router = APIRouter()

print(AppConfig.DEBUG)
app = FastAPI(
    docs_url="/docs" if AppConfig.DEBUG else None,
    redoc_url="/redoc" if AppConfig.DEBUG else None,
    openapi_url="/openapi.json" if AppConfig.DEBUG else None
)

Base.metadata.create_all(bind=engine)


app.include_router(router=user_router)

@app.get("/")
def health_check():
    return{ 
        "status":"success",
        "message":"User service is up and running"
    } 


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="src.app.user.main:app", 
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        reload=True
    )
