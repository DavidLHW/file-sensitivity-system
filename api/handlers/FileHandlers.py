import logging
import os
from datetime import datetime

from flask import request, current_app
from flask_restful import Resource

from werkzeug.utils import secure_filename

import api.error.errors as error
from api.conf.auth import auth
from api.database.database import db_session
from api.schemas.schemas import FileSchema


class UploadFile(Resource):
    @auth.login_required
    def post(self):
        # receive file
        uploaded_file = request.files['file']
        filename = uploaded_file.filename

        # if file dont exist
        if filename == '':
            return error.NO_INPUT_400

        # get file extension
        file_ext = os.path.splitext(filename)[1]

        # if file extension is not valid
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            return error.INVALID_INPUT_422

        # calculate file size
        uploaded_file.seek(0, os.SEEK_END)
        file_length = uploaded_file.tell()
        uploaded_file.seek(0, 0)
        file_size = str(round(file_length / (1024 * 1024), 2)) + "MB"

        # save file
        file_storage_dir = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(file_storage_dir, secure_filename(filename))
        uploaded_file.save(file_path)

        return {
            "filename":     uploaded_file.filename,
            "content-type": uploaded_file.content_type,
            "file size":    file_size
        }