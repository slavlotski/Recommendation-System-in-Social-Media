from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from table_user import User
from table_post import Post
from database import Base
# Создаем таблицу FEED_DATA из БД как объект SQLALCHEMY 
class Feed(Base):
    __tablename__ = 'feed_data'

    user_id = Column(Integer,ForeignKey(User.user_id),primary_key=True,name="user_id")
    user = relationship(User)
    post_id = Column(Integer,ForeignKey(Post.post_id),primary_key=True,name="post_id")
    post = relationship(Post)
    action = Column(String)
    time = Column(DateTime)