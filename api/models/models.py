from datetime import datetime

from flask import g

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from api.conf.auth import auth, jwt

# Create sql alchemy database object.
Base = declarative_base()

class User(Base):

    # Generates default class name for table.
    __tablename__ = 'users'

    # User id.
    id = Column(Integer, primary_key=True)

    # User name.
    username = Column(String(length=80))

    # User password.
    password = Column(String(length=80))

    # User email address.
    email = Column(String(length=80))

    # Creation time for user.
    created = Column(DateTime, default=datetime.utcnow)

    # Generates auth token.
    def generate_auth_token(self):
        # Return normal user flag.
        return jwt.dumps({"email": self.email})

    # Generates a new access token from refresh token.
    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):

        # Create a global none user.
        g.user = None

        try:
            # Load token.
            data = jwt.loads(token)

        except:
            # If any error return false.
            return False

        # Check if email and admin permission variables are in jwt.
        if "email" in data:

            # Set email from jwt.
            g.user = data["email"]

            # Return true.
            return True

        # If does not verified, return false.
        return False

    def __repr__(self):

        # This is only for representation to see after query.
        return "<User(id='%s', name='%s', password='%s', email='%s', created='%s')>" % (
            self.id,
            self.username,
            self.password,
            self.email,
            self.created,
        )


class Blacklist(Base):

    # Generates default class name for table.
    __tablename__ = 'blacklist'

    # Blacklist id.
    id = Column(Integer, primary_key=True)

    # Blacklist invalidated refresh tokens.
    refresh_token = Column(String(length=255))

    def __repr__(self):

        # This is only for representation how you want to see refresh tokens after query.
        return "<User(id='%s', refresh_token='%s', status='invalidated.')>" % (
            self.id,
            self.refresh_token,
        )


class File(Base):

    # Generates default class name for table.
    __tablename__ = 'files'

    # User id.
    id = Column(Integer, primary_key=True)

    # File name.
    filename = Column(String(length=80))

    # File size in bytes.
    filesize = Column(Integer)

    # File path.
    filepath = Column(String)

    # File sensitivity score.
    score = Column(Integer, default=-1)

    # Last updated time for file.
    updated = Column(DateTime, default=datetime.utcnow)

    # Uploaded time for file.
    uploaded = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):

        # Create a global none user.
        g.user = None

        try:
            # Load token.
            data = jwt.loads(token)

        except:
            # If any error return false.
            return False

        # Check if email and admin permission variables are in jwt.
        if "email" in data:

            # Set email from jwt.
            g.user = data["email"]

            # Return true.
            return True

        # If does not verified, return false.
        return False

    def __repr__(self):

        # This is only for representation how you want to see after query.
        return "<File(id='%s', name='%s', size='%s', path='%s', uploaded='%s')>" % (
            self.id,
            self.filename,
            self.filesize,
            self.filepath,
            self.uploaded,
        )