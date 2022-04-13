from mongoengine import StringField, ReferenceField, ListField, DictField, IntField, DateTimeField, BooleanField
from mongoengine import Document


class Application(Document):
    bundle_id = StringField(unique=True, required=True)
    name = StringField(required=True)
    version = StringField(required=True)
    meta = {"collection": "applications"}


class User(Document):
    dis_id = IntField(unique=True, required=True)
    meta = {"collection": "users"}


class Role(Document):
    name = StringField(unique=True, required=True)
    emoji = StringField(unique=True, required=True)
    role_id = IntField(unique=True, required=True)
    exclusive = StringField()


class Points(Document):
    user = ReferenceField(User, required=True)
    type = StringField(required=True)
    points = IntField(required=True)
    meta = {"collection": "points"}


class Tag(Document):
    name = StringField(unique=True, required=True)
    tag = StringField(required=True)
    section = StringField()
    meta = {"collection": "tags"}


class CommandUsage(Document):
    command = StringField(required=True)
    user = ReferenceField(User, required=True)
    times = IntField()
    meta = {"collection": "command_uses"}


class Timeout(Document):
    user = ReferenceField(User, required=True)
    reason = StringField(required=True)
    until = DateTimeField(required=True)
    meta = {"collection": "timeouts"}
