from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import DATABASE
from src.db.models import Base

engine = create_engine('postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db_name}'
                       .format(user=DATABASE['username'],
                               pwd=DATABASE['password'],
                               host=DATABASE['hostname'],
                               port=DATABASE['port'],
                               db_name=DATABASE['database']),
                       client_encoding='utf8', echo=True, pool_size=DATABASE['max_pool'], max_overflow=0)


def init_db():
    Base.metadata.create_all(bind=engine)


def db_session():
    return sessionmaker(bind=engine)
