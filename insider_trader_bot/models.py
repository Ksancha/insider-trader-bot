from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey



Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    username = Column(String)
    chat_id = Column(Integer, unique=True, primary_key=True, autoincrement=False)


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class UserStocks(Base):
    __tablename__ = "user_stocks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.chat_id', ondelete="CASCADE"))
    stock_id = Column(Integer, ForeignKey('stocks.id', ondelete="CASCADE"))


if __name__ == '__main__':
    pass
    # folder = os.path.dirname(__file__)
    # engine = create_engine("sqlite:////" + os.path.join(folder, "pythonsqlite.db"))
    # Base.metadata.create_all(engine)
