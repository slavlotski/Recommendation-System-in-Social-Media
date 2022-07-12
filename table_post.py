from sqlalchemy import Column, Integer, String
from database import Base
# Создаем таблицу POST_TEXT_DF из БД как объект SQLALCHEMY 
class Post(Base):
    __tablename__ = 'post_text_df'
    post_id = Column(Integer,primary_key=True,name="post_id")
    text = Column(String)
    topic = Column(String)
