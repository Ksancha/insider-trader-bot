import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def init_session():
    folder = os.path.dirname(__file__)
    engine = create_engine("sqlite:////" + os.path.join(folder, "pythonsqlite.db"))

    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    return session
