from marshmallow import Schema, fields

class ShortURLSchema(Schema):
    id = fields.Int(dump_only=True)
    long_url = fields.Str(required=True)
    short_url = fields.Str(dump_only=True)
    domain_name = fields.Str(required=True)

class HistorySchema(Schema):
    id = fields.Int(dump_only=True)
    long_url = fields.Str(dump_only=True)
    short_url = fields.Str(dump_only=True)
    domain_name = fields.Str(dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    confirm_password = fields.Str(required=True)
    
class UsersSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class ClickSchema(Schema):
    id = fields.Int(dump_only=True)
    long_url = fields.String(dump_only=True)
    short_url = fields.String(dump_only=True)
    domain_name = fields.String(dump_only=True)
    clicks = fields.Int(dump_only=True)
    user_agent = fields.String(dump_only=True)
    referrer = fields.String(dump_only=True)
    clicked_at = fields.DateTime(dump_only=True)
    ip_address = fields.String(dump_only=True)




