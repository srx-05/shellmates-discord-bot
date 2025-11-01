import logging
from datetime import datetime


#Set up logging for debugging & monitoring
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler()
        ]
    )


# Format timestamps consistently year-month-day hour:minute:second
def format_date(date: datetime) -> str:
    return date.strftime('%Y-%m-%d %H:%M:%S')


# Prevent overly long strings
def truncate_text(text: str, max_length: int = 100) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'