import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', "6251329523:AAFRYhYyoEYIkI-lIrpfkLeUla2g7lujv0I")
ADMIN_IDS = [int(id) for id in os.getenv('ADMIN_IDS', '6045293810').split(',') if id]
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///games.db')
