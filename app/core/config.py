import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Settings:
    PROJECT_NAME: str = "My FastAPI Project"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

settings = Settings()
