import os

DATABASE = {
    'hostname': os.getenv("DB_HOSTNAME", 'localhost'),
    'port': 5432,
    'database': os.getenv("POSTGRES_DB", "calc"),
    'min_pool': 10,
    'max_pool': 24,
    'username': os.getenv('POSTGRES_USER', 'user'),
    'password': os.getenv('POSTGRES_PASSWORD', "password")
}

AVAILABLE_STATUS = ["fail", "success"]