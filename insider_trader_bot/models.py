import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    username = Column(String(16))
    chat_id = Column(Integer, unique=True, primary_key=True, autoincrement=False)
    subscribed_to_buys = Column(Boolean, default=False)


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True)


class UserStocks(Base):
    __tablename__ = "user_stocks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.chat_id', ondelete="CASCADE"))
    stock_id = Column(Integer, ForeignKey('stocks.id', ondelete="CASCADE"))


if __name__ == '__main__':
    from sqlalchemy import create_engine
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    engine = create_engine(f"mysql://{user}:{password}@localhost/telegram_bot")
    Base.metadata.create_all(engine)
