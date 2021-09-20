from marshmallow import Schema, fields


class FileSchema(Schema):

    """
    User schema returns only username, email and creation time. This was used in user handlers.
    """

    # Schema parameters.

    name = fields.Str()
    size = fields.Int(dump_only=True)
    path = fields.Str()
    upload = fields.Str()