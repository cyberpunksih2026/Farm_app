from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="SIH26033 Farmer-Buyer Logistics API",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "project": "SIH26033",
        "message": "Farmer-Buyer Logistics API is running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
