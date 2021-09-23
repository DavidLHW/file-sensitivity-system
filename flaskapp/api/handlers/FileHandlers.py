import logging
import os

from flask import request, current_app
from flask_restful import Resource

from werkzeug.utils import secure_filename

import api.error.errors as error
from api.conf.auth import auth
from api.models.models import File
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

        # format filesize to be human readable
        filesize = file_length
        suffixes=['B','kB','MB']
        suffixIndex = 0
        while filesize > 1024 and suffixIndex < len(suffixes)-1:
            suffixIndex += 1 #increment the index of the suffix
            filesize = filesize/1024.0 #apply the division

        filesize = "%.*f %s"%(1, filesize, suffixes[suffixIndex])

        # Save file locally.
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(upload_folder, secure_filename(filename))
        uploaded_file.save(filepath)

        # Ceate a new file.
        file = File(
                filename=filename,
                filesize=file_length,
                filepath=filepath)

        try:
            # Add user to session.
            db_session.add(file)

            # Commit session.
            db_session.commit()

            # Close DB session to prevent memory leaks.
            db_session.close()

        except Exception as why:
            # Log the error.
            logging.error(why)
            return error.INVALID_INPUT_422

        return {
            "filename":     filename,
            "content-type": uploaded_file.content_type,
            "file size":    filesize
        }

class ListFile(Resource):
    @auth.login_required
    def get(self):
        # retrieve file from DB
        files = db_session.query(File).all()

        try:
            # return files
            file_schema = FileSchema()
            data = file_schema.dump(files, many=True)

        except Exception as why:
            # Log the error.
            logging.error(why)
            return error.SERVER_ERROR_500

        return data

