from dotenv import load_dotenv
from db_config import db
import os

load_dotenv()

MYSQL_HOST= os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')
SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig:
    DEBUG = True
    MYSQL_HOST = MYSQL_HOST  # Tomando las variables de entorno
    MYSQL_USER = MYSQL_USER
    MYSQL_PASSWORD = MYSQL_PASSWORD
    MYSQL_DB = MYSQL_DB
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'sqlalchemy'
    SESSION_SQLALCHEMY = db
    SESSION_USE_SIGNER = True
    SESSION_SQLALCHEMY_TABLE = 'flask_sessions'
    



config = {
    'development': DevelopmentConfig
}