import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URI', 'Database connection string is missing')
DEFAULT_DATABSE_URI = os.getenv(
    'DEFAULT_DATABASE_URI', 'Database connection string is missing')
DATABASE_NAME = os.getenv('DATABASE_NAME')
SCHEMA_NAME = os.getenv('SCHEMA_NAME')
PROJECT_NAME = os.getenv('PROJECT', 'Watchtower')
DESCRIPTION = os.getenv('DESCRIPTION')
ROOT_USER = os.getenv('ROOT_USER')
ROOT_USER_PASSWORD = os.getenv('ROOT_USER_PASSWORD')
ENCRYPTION = os.getenv('ENCRYPTION')
TOKEN_EXPIRY = os.getenv('TOKEN_EXPIRY')
TOKEN_SECRET = os.getenv('TOKEN_SECRET')
