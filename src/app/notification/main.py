from fastapi import FastAPI


app = FastAPI()

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Notification service is running."
    }


