import os

DATABASE = {
    'hostname': 'postgres',
    'port': 5432,
    'database': os.getenv("POSTGRES_DB", "calc"),
    'min_pool': 10,
    'max_pool': 24,
    'username': os.getenv('POSTGRES_USER', 'user'),
    'password': os.getenv('POSTGRES_PASSWORD', "password")
}

AVAILABLE_STATUS = ["fail", "success"]