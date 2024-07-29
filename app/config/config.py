import os

from dotenv import load_dotenv
from flask import Flask


class Config:
    load_dotenv()
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    TOKEN_TG_BOT = os.getenv('TOKEN_TG_BOT')
    ID_CHAT_TG = os.getenv('ID_CHAT_TG')
    TOKEN_GROUP_VK = os.getenv('TOKEN_GROUP_VK')
    ID_GROUP_VK = os.getenv('ID_GROUP_VK')
    HREF_STUDIO = os.getenv('HREF_STUDIO')
    SERVER_NAME = '127.0.0.1:8000'


def apply_settings(app: Flask):
    app.config.from_object(Config)