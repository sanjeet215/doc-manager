from fastapi import FastAPI
from app.api.routes import router
from .core.logging_config import setup_logging

# Get a logger instance
logger = setup_logging()
app = FastAPI()

# Include your API routes
app.include_router(router)

@app.get("/")
async def root():
    logger.info("INFO:Loger setup is working")
    logger.debug("DEBUG:Loger setup is working")
    return {"message": "Welcome to the API"}
