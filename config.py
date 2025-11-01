import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    # Discord Configuration
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    COMMAND_PREFIX = "/" 
    
    # # DB Configuration
    DATABASE_URL = os.getenv("DATABASE_URL")
   
    @classmethod
    def validate(cls):
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN is not set in environment variables")
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set in environment variables")
