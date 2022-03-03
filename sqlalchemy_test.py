from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    user_id = Column("id", Integer, primary_key=True)
    username = Column("username", String, unique=True)
    posts = relationship("Post")

class Post(Base):

    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = Column(Integer, ForeignKey("users.username"))



engine = create_engine('sqlite:///test_database.db', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

current_session = Session()

user = User()
user.user_id = 1
user.username = "Pete"

current_session.add(user)
current_session.commit()

current_session.close()