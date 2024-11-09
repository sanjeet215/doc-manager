from fastapi import FastAPI
from app.api.routes import router

app = FastAPI()

# Include your API routes
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
