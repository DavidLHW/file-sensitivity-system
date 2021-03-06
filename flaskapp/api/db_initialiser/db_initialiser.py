import logging
import sys

sys.path.append("..")

from flaskapp.api.models.models import Base
from flaskapp.api.database.database import db_session, engine
from flaskapp.api.models.models import User, File
from flaskapp.api.conf.auth import generate_password_hash

from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy_utils import database_exists, create_database

def initialise_database(
    email="test_email@example.com",
    filepath="path/to/file/test.txt"
):    
    # Create database if it doesn't exist.
    if not database_exists(engine.url):
        create_database(engine.url)

    try:
        # Check if user exists in db.
        user = db_session.query(User).filter_by(email=email).first()

        # Check if user exists in db.
        file = db_session.query(File).filter_by(filepath=filepath).first()

    except:
        user = None
        file = None

    if user or file:
        print('DROPPING', user, file)
        
        # Closes all sessions.
        close_all_sessions()

        # Drops the previously populated database on restart.
        Base.metadata.drop_all(engine)

        # Creates new tables.
        Base.metadata.create_all(engine)
    
    else:
        # Creates new tables.
        Base.metadata.create_all(engine)

    # Closes all sessions once done.
    close_all_sessions()



def create_test_user(
    username="test_username",
    password=generate_password_hash("test_password"),
    email="test_email@example.com"
):
    # Check if user exists in db.
    user = db_session.query(User).filter_by(email=email).first()

    # If user is none.
    if not user:
        # Create user if it does not exists.
        user = User(
            username=username,
            password=password,
            email=email
        )

        # Add user to session.
        db_session.add(user)

        # Commit session.
        db_session.commit()

        # Print admin user status.
        logging.info("Test user was set.")

        # Return user.
        return user

    else:

        # Print admin user status.
        logging.info("User already set.")

    # Close DB session to prevent memory leaks.
    db_session.close()


def create_test_file(
    filename="test_file",
    filesize=1024,
    filepath="path/to/file/test.txt"
):
    # Check if file exists in db.
    file = db_session.query(File).filter_by(filepath=filepath).first()

    # If file is none.
    if not file:

        # Create File if it does not exist.
        file = File(
            filename=filename,
            filesize=filesize,
            filepath=filepath
        )

        # Add user to session.
        db_session.add(file)

        # Commit session.
        db_session.commit()

        # Print admin user status.
        logging.info("Test user was set.")

        # Return user.
        return file

    else:

        # Print admin user status.
        logging.info("User already set.")

    # Close DB session to prevent memory leaks.
    db_session.close()
