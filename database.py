from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
#Подгружаем все переменные окружения
load_dotenv(".env")
SQLALCHEMY_DATABASE_URL = os.environ("connection_url")
#Создаем подключение к БД
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
session = SessionLocal()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
