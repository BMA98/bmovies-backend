import os

SECRET_KEY = os.getenv('SECRET_KEY')
TMDB_KEY = os.getenv('TMDB_KEY')

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

DEBUG_MODE = os.getenv('DEBUG_MODE', False)

ALLOWED_HOST = os.getenv('ALLOWED_HOST')
