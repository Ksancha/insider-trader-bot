import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def init_session():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    engine = create_engine(f"mysql://{user}:{password}@localhost/telegram_bot")
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    return session


session = init_session()
