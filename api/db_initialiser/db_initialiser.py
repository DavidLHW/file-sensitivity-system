import logging

from api.database.database import db_session
from api.models.models import User, File


def create_test_user(
    username="test_username",
    password="test_password",
    email="test_email@example.com",
    user_role="user",
):

    # # Initialise DB session.
    # db_session = Session()

    # Check if admin is existed in db.
    user = db_session.query(User).filter_by(email=email).first()

    print(user)

    # If user is none.
    if user is None:

        # Create admin user if it does not existed.
        # user = User(username=username, password=password, email=email, user_role=user_role)
        user = User(
            username=username,
            password=password,
            email=email,
            user_role=user_role,
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


def create_test_user(
    filename="test_file",
    filesize=1024,
    filepath="path/to/file/text.txt"
):

    # # Initialise DB session.
    # db_session = Session()

    # Check if admin is existed in db.
    file = db_session.query(File).filter_by(filepath=filepath).first()

    print(file)

    # If user is none.
    if file is None:

        # Create admin user if it does not existed.
        # user = User(username=username, password=password, email=email, user_role=user_role)
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