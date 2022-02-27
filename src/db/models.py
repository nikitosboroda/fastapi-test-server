from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    status = Column(String(15))
    request = Column(String(255))
    response = Column(String(255), default="", nullable=True)

    def to_json(self, exclude_fields: tuple = ()) -> dict:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns if column.name not in exclude_fields
        }
