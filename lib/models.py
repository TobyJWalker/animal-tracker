import peewee, os
from hashlib import sha256
from datetime import datetime

if os.environ.get('APP_ENV') == 'test':
    db = peewee.SqliteDatabase('test-db.sqlite3')
else:
    db = peewee.SqliteDatabase('animal-info.sqlite3')


class User(peewee.Model):
    username = peewee.CharField(unique=True)
    password = peewee.CharField()

    class Meta:
        database = db
        table_name = 'users'

    def __str__(self):
        return self.username

    @staticmethod
    def hash_password(password):
        return sha256(password.encode('utf-8')).hexdigest()


class Animal(peewee.Model):
    name = peewee.CharField()
    species = peewee.CharField()
    age = peewee.IntegerField()
    date_of_birth = peewee.DateField()
    weight = peewee.FloatField()
    height = peewee.FloatField()
    length = peewee.FloatField()
    personality = peewee.CharField()
    tag = peewee.CharField()
    group = peewee.CharField()
    owner = peewee.ForeignKeyField(User, backref='animals')

    class Meta:
        database = db
        table_name = 'animals'

    def __str__(self):
        return self.name


class Notes(peewee.Model):
    content = peewee.TextField()
    animal = peewee.ForeignKeyField(Animal, backref='notes')

    class Meta:
        database = db
        table_name = 'notes'

    def __str__(self):
        return self.content

def create_db_tables():
    with db:
        db.create_tables([User, Animal, Notes])

if __name__ == '__main__':
    create_db_tables()
