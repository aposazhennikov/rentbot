from os import getenv

# DB credentials
DB_HOST = getenv('DB_HOST')
DB_NAME = getenv('DB_NAME')
DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
# DB_PORT = int(getenv('DB_PORT')) #default is set already 5432

# Bot token
BOT_TOKEN = getenv('BOT_TOKEN')
BOT_MODE = 'dev'  # prod
