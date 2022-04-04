import os
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')


