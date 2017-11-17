import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('taco.db')


class User(UserMixin, Model):
    """This is the model for a user."""
    email = CharField(unique=True)
    password = CharField(max_length=35)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('joined_at',)

    @classmethod
    def create_user(cls, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


class Taco(Model):
    """ This is the model for a taco. Yum!"""
    user = ForeignKeyField(
        rel_model=User,
        related_name='user'
    )
    timestamp = DateTimeField(default=datetime.datetime.now)
    protein = CharField()
    shell = CharField()
    cheese = CharField()
    extras = CharField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Taco], safe=True)
    DATABASE.close()
