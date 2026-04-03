from fastapi import FastAPI
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance & Access Control API",
    description="Backend Assignment for Zorvyn Internship",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"status": "success", "message": "Finance API is online"}
