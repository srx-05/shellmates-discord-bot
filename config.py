import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    # Discord Configuration
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN") or ""
    COMMAND_PREFIX: str = "/"
 
    
    # DB Configuration
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")
    DB_HOST : str | None = os.getenv("DB_HOST")
    DB_PORT: str | None = os.getenv("DB_PORT")
    DB_NAME: str | None = os.getenv("DB_NAME")
    DB_USER: str | None = os.getenv("DB_USER")
    DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
    DB_POOL_MIN: int = int( os.getenv("DB_POOL_MIN","5"))
    DB_POOL_MAX: int = int(os.getenv("DB_POOL_MAX","20"))
  
   
    @classmethod
    def validate(cls):
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN is not set in environment variables")
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set in environment variables")
