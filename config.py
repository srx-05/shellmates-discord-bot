import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    # Discord Configuration
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    COMMAND_PREFIX = "!" 
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGO_URI')
    MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
    
    @classmethod
    def validate(cls):
        if not cls.TOKEN:
            raise ValueError("DISCORD_TOKEN is not set in environment variables")
        if not cls.MONGODB_URI:
            raise ValueError("MONGODB_URI is not set in environment variables")