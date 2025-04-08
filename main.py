from peewee import *
import datetime
import uuid

db = SqliteDatabase('./db/zigbee.db')

class Sensor(Model):
    uuid = UUIDField(primary_key=True, default=uuid.uuid4())


class User(Model):
    username = CharField(unique=True)
    email = CharField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def main():
    db.connect()
    db.create_tables([User], safe=True)

    try:
        new_user = User.create(
            username='john_doe',
            email='john@example.com'
        )
        print(f"Created new user with ID: {new_user.id}")
    except IntegrityError:
        print("User already exists")

    print("\nAll users in database:")
    for user in User.select():
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Created: {user.created_at}")

    db.close()


if __name__ == '__main__':
    main()