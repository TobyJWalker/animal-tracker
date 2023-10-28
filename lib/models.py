import peewee, os
from hashlib import sha256
from datetime import datetime

if os.environ.get('APP_ENV') == 'test':
    db = peewee.SqliteDatabase('test-db.sqlite3')
else:
    db = peewee.SqliteDatabase('animal-info.sqlite3')


class User(peewee.Model):
    username = peewee.CharField(unique=True)
    email = peewee.CharField()
    password = peewee.CharField()

    class Meta:
        database = db
        table_name = 'users'

    def __str__(self):
        return self.username

    @staticmethod
    def hash_password(password):
        return sha256(password.encode('utf-8')).hexdigest()
    
    @staticmethod
    def check_login(username, password):
        try:
            user = User.get(User.username == username)
            if user.password == User.hash_password(password):
                return user
            else:
                return None
        except:
            return None


class Animal(peewee.Model):
    name = peewee.CharField()
    species = peewee.CharField()
    colour = peewee.CharField()
    age = peewee.IntegerField()
    date_of_birth = peewee.DateField()
    weight = peewee.FloatField()
    height = peewee.FloatField()
    length = peewee.FloatField()
    personality = peewee.CharField()
    tag = peewee.CharField()
    group = peewee.CharField()
    img_url = peewee.CharField()
    owner = peewee.ForeignKeyField(User, backref='animals')

    class Meta:
        database = db
        table_name = 'animals'

    def __str__(self):
        return self.name
    
    def get_animals_by_user_id(user_id):
        return Animal.select().where(Animal.owner == user_id)


class Notes(peewee.Model):
    content = peewee.TextField()
    animal = peewee.ForeignKeyField(Animal, backref='notes')

    class Meta:
        database = db
        table_name = 'notes'

    def __str__(self):
        return self.content

class Group(peewee.Model):
    name = peewee.CharField()
    animals = peewee.ManyToManyField(Animal, backref='groups')

    class Meta:
        database = db
        table_name = 'groups'

    def __str__(self):
        return self.name

def create_db_tables():
    with db:
        db.create_tables([User, Animal, Notes])

if __name__ == '__main__':
    create_db_tables()
