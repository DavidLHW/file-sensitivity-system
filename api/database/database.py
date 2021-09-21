from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.conf.config import DATABASE_URI
from api.models.models import Base


# Engine object.
engine = create_engine(DATABASE_URI)

# Session object, not initialised.
Session = sessionmaker(bind=engine)

db_session = Session()