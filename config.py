import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
load_dotenv()

TG_KEY = os.getenv('TG_API')
PASSWORD_ADMIN = os.getenv('PASSWORD_ADMIN')

HOST = os.getenv('HOST')
USER_DB = os.getenv('USER_DB')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
PG_PORT = os.getenv('DATABASE_PORT') if os.getenv('DATABASE_PORT') else 5432


bot = Bot(token=TG_KEY, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
