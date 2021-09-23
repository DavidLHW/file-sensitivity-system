import logging
import sys

sys.path.append("..")

from flask import request
from flask_restful import Resource

import flaskapp.api.error.errors as error
from flaskapp.api.database.database import db_session
from flaskapp.api.models.models import User, Blacklist
from flaskapp.api.conf.auth import (
    auth,
    refresh_jwt,
    generate_password_hash,
    check_password_hash
)


class Index(Resource):
    @staticmethod
    def get():
        return "File Sensitivity System"


class Register(Resource):
    @staticmethod
    def post():

        try:
            # Get username, password and email.
            username, password, email = (
                request.json.get("username").strip(),
                request.json.get("password").strip(),
                request.json.get("email").strip(),
            )
        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Username, password or email is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if any field is none.
        if not (username and email and password):
            return error.INVALID_INPUT_422

        # Get user if user existsd.
        user = db_session.query(User).filter_by(email=email).first()

        # Check if user exists.
        if user is not None:
            return error.ALREADY_EXIST

        # Create a new user.
        user = User(
                username=username,
                password=generate_password_hash(password),
                email=email)

        try:
            # Add user to session.
            db_session.add(user)

            # Commit session.
            db_session.commit()

        except Exception as why:
            # Log the error.
            logging.error(why)
            return error.INVALID_INPUT_422

        # Close DB session to prevent memory leaks.
        db_session.close()

        # Return success if registration is completed.
        return {"status": "registration completed."}


class Login(Resource):
    @staticmethod
    def post():

        try:
            # Get user email and password.
            email, password = (
                request.json.get("email").strip(),
                request.json.get("password").strip(),
            )

        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Email or password is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if user information is none.
        if not(email and password):
            return error.INVALID_INPUT_422

        # # Initialise DB session.
        # db_session = Session()

        # Get user if it is exists.
        user = db_session.query(User).filter_by(email=email).first()

        # Close DB session to prevent memory leaks.
        db_session.close()

        # If user does not exist or if incorrect password.
        if not user or not check_password_hash(user.password, password):
            print(user.password, password)
            return error.UNAUTHORIZED

        else:
            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
            access_token = user.generate_auth_token()

        # Generate refresh token.
        refresh_token = refresh_jwt.dumps({"email": email})

        # Return access token and refresh token.
        return {
            "access_token": access_token.decode(),
            "refresh_token": refresh_token.decode(),
        }


class Logout(Resource):
    @staticmethod
    @auth.login_required
    def post():

        # Get refresh token.
        refresh_token = request.json.get("refresh_token")

        # # Initialise DB session.
        # db_session = Session()

        # Get if the refresh token is in blacklist.
        ref = db_session.query(Blacklist).filter_by(refresh_token=refresh_token).first()

        # Check if refresh token exists.
        if ref is not None:
            return {"status": "already invalidated", "refresh_token": refresh_token}

        # Create a blacklist refresh token.
        blacklist_refresh_token = Blacklist(refresh_token=refresh_token)

        # Add refresh token to session.
        db_session.add(blacklist_refresh_token)

        # Commit session.
        db_session.commit()

        # Close DB session to prevent memory leaks.
        db_session.close()

        # Return status of refresh token.
        return {"status": "invalidated", "refresh_token": refresh_token}


class RefreshToken(Resource):
    @staticmethod
    def post():

        # Get refresh token.
        refresh_token = request.json.get("refresh_token")

        # # Initialise DB session.
        # db_session = Session()

        # Get if the refresh token is in blacklist.
        ref = db_session.query(Blacklist).filter_by(refresh_token=refresh_token).first()

        # Close DB session to prevent memory leaks.
        db_session.close()

        # Check if refresh token exists.
        if ref is not None:

            # Return invalidated token.
            return {"status": "invalidated"}

        try:
            # Generate new token.
            data = refresh_jwt.loads(refresh_token)

        except Exception as why:
            # Log the error.
            logging.error(why)

            # If it does not generated return false.
            return False

        # Create user not to add db. For generating token.
        user = User(email=data["email"])

        # New token generate.
        token = user.generate_auth_token()

        # Return new access token.
        return {"access_token": token}

# auth.login_required: Auth is necessary for this handler.