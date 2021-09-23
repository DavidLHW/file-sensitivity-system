import sys

sys.path.append("..")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flaskapp.api.conf.config import DATABASE_URI


# Engine object.
engine = create_engine(DATABASE_URI)

# Session object, not initialised.
Session = sessionmaker(bind=engine)

db_session = Session()