# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
