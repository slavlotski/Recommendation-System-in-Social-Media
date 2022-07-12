from sqlalchemy import Column, Integer, String
from database import Base
# Создаем таблицу USER_DATA из БД как объект SQLALCHEMY 
class User(Base):
    __tablename__ = 'user_data'

    user_id = Column(Integer,primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)
