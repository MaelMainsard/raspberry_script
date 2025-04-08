from peewee import *
import uuid
import datetime

db = SqliteDatabase('./db/zigbee.db')

class NodeParam(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True, null=False)
    updated_at = DateTimeField(default=datetime.datetime.now)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

class NodeData(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    node_id = ForeignKeyField(NodeParam, backref='data')
    temperature = FloatField(null=True)
    humidity = FloatField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db