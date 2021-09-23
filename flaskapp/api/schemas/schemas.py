from marshmallow import Schema, fields


class FileSchema(Schema):

    """
    File schema returns only filename, filesize, filepath and uploaded time.
    This is used in FileHandler
    """

    # Schema parameters.
    filename = fields.Str()
    filesize = fields.Int(dump_only=True)
    filepath = fields.Str()
    score = fields.Int(dump_only=True)
    last_updated = fields.DateTime()

    # Used to preserve ordering.
    class Meta:
        ordered = True