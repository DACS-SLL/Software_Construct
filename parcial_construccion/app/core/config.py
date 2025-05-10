### config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "JobHub API"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

settings = Settings()