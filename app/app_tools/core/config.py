import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path("./")/".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):

    # App
    APP_NAME: str = os.environ.get('APP_NAME', 'Portfolio')
    DEBUG: bool = bool(os.environ.get("DEBUG", False))
    COMPANY_NAME: str = os.environ.get("COMPANY_NAME")
    COMPANY_EMAIL: str = os.getenv("COMPANY_EMAIL")

    # Frontend App
    FRONTEND_HOST: str = os.getenv("FRONTEND_HOST")

    # Database
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: str = os.getenv('DB_PORT')
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    REDIS_PORT: str = os.getenv('REDIS_PORT')
    REDIS_HOST: str = os.getenv('REDIS_HOST')

    # App Secret key
    SECRET_KEY: str = os.environ.get("SECRET_KEY")

Settings()
