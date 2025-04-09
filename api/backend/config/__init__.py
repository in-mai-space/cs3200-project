import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    
    config = {
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'MYSQL_DATABASE_USER': os.getenv('DB_USER'),
        'MYSQL_DATABASE_PASSWORD': os.getenv('MYSQL_ROOT_PASSWORD'),
        'MYSQL_DATABASE_HOST': os.getenv('DB_HOST'),
        'MYSQL_DATABASE_PORT': int(os.getenv('DB_PORT')),
        'MYSQL_DATABASE_DB': os.getenv('DB_NAME')
    }
    
    return config