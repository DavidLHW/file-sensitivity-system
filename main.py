import os

from flask import Flask

# from api.conf.config import SQLALCHEMY_DATABASE_URI
from api.conf.routes import generate_routes
from api.database.database import initialise_database
from api.db_initialiser.db_initialiser import create_test_user, create_test_file


def create_app():

    # Create a flask app.
    app = Flask(__name__)

    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, "files")

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    print(UPLOAD_FOLDER)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Set debug true for catching the errors.
    app.config['DEBUG'] = True

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # allow max 500MB of file size.
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

    app.config['UPLOAD_EXTENSIONS'] = ['.txt']

    # Generate routes.
    generate_routes(app)

    # Create and initialise database if database don't already exist
    initialise_database()

    # Create default test user in database.
    create_test_user()

    # Create default test file in database.
    create_test_file()

    # Return app.
    return app


if __name__ == '__main__':

    # Create app.
    app = create_app()

    # Run app. For production use another web server.
    # Set debug and use_reloader parameters as False.
    app.run(port=5000, debug=True, host='localhost', use_reloader=True)