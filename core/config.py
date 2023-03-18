import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

FRONTEND_URL = os.getenv('FRONTEND_URL')

# postgresql
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URI', 'Database connection string is missing')
DEFAULT_DATABASE_URI = os.getenv(
    'DEFAULT_DATABASE_URI', 'Default database connection string is missing')
DATABASE_NAME = os.getenv('DATABASE_NAME')
SCHEMA_NAME = os.getenv('SCHEMA_NAME')

# project
PROJECT_NAME = os.getenv('PROJECT', 'Watchtower')
DESCRIPTION = os.getenv('DESCRIPTION')
ROOT_USER = os.getenv('ROOT_USER')
ROOT_USER_PASSWORD = os.getenv('ROOT_USER_PASSWORD')
PASSWORD_LIMIT = os.getenv('PASSWORD_LIMIT')
PASSWORD_EXPIRY = os.getenv('PASSWORD_EXPIRY')

# token
ENCRYPTION = os.getenv('ENCRYPTION')
TOKEN_NAME = os.getenv('TOKEN_NAME')
TOKEN_EXPIRY = os.getenv('TOKEN_EXPIRY')
