from peewee import (
    Model, PrimaryKeyField, SqliteDatabase, CharField
)


database = SqliteDatabase(':memory:', autocommit=False)

database.connect()


class StandardModel(Model):
    id = PrimaryKeyField()
    foo = CharField()


class NonIntegerPk(Model):
    id = CharField(primary_key=True)


if StandardModel.table_exists():
    StandardModel.drop_table()
StandardModel.create_table()
if NonIntegerPk.table_exists():
    NonIntegerPk.drop_table()
NonIntegerPk.create_table()
