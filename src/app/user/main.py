from fastapi import FastAPI
from fastapi.routing import APIRouter
from config.config import AppConfig

from application.user_controller import router as user_router
from database import engine, Base
import schema

router = APIRouter()
app = FastAPI()



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
        app=app,
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        # reload=AppConfig.DEBUG
    )
