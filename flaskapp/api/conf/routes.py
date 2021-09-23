import sys

sys.path.append("..")

from flask_restful import Api

from flaskapp.api.handlers.FileHandlers import (
    UploadFile,
    ListFile)
from flaskapp.api.handlers.UserHandlers import (
    Index,
    Login,
    Logout,
    Register)

def format_route_url(route):
    return "/api/" + route

def generate_routes(app):

    # Create api.
    api = Api(app)

    # Add all routes resources.
    # Index page.
    api.add_resource(Index, "/")

    # Register page.
    api.add_resource(Register, format_route_url("auth/register"))

    # Login page.
    api.add_resource(Login, format_route_url("auth/login"))

    # Logout page.
    api.add_resource(Logout, format_route_url("auth/logout"))

    # Get file page with auth.
    api.add_resource(UploadFile, format_route_url("file"))

    # Get files page with auth.
    api.add_resource(ListFile, format_route_url("files"))