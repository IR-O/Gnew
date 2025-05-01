import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Required configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN', "6251329523:AAFRYhYyoEYIkI-lIrpfkLeUla2g7lujv0I")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN must be set in environment variables")
    
    # Optional configuration with defaults
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    ADMIN_IDS = [int(id) for id in os.getenv('ADMIN_IDS', "6045293810").split(',') if id]
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    PORT = int(os.getenv('PORT', 8443))
    
    # Game settings
    TRIVIA_TIME_LIMIT = 30
    WORDCHAIN_TIME_LIMIT = 20
    MAX_SCORES = 1000
