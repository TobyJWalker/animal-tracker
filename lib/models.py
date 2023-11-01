import peewee, os
from hashlib import sha256
from datetime import datetime

# create the peewee db object
if os.environ.get('APP_ENV') == 'test':
    db = peewee.SqliteDatabase('test-db.sqlite3')
else:
    dbname = os.environ.get('POSTGRES_DB')
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')

    db = peewee.PostgresqlDatabase(dbname, user=user, password=password, host='postgres', port=5432)


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
    colour = peewee.CharField(null=True)
    age = peewee.IntegerField(null=True)
    date_of_birth = peewee.DateField(null=True)
    weight = peewee.FloatField(null=True)
    weight_type = peewee.CharField(default='kg')
    height = peewee.FloatField(null=True)
    height_type = peewee.CharField(default='m')
    length = peewee.FloatField(null=True)
    length_type = peewee.CharField(default='m')
    personality = peewee.CharField(null=True)
    tag = peewee.CharField(null=True)
    group = peewee.CharField(null=True)
    img_url = peewee.CharField(null=True)
    owner = peewee.ForeignKeyField(User, backref='animals')

    class Meta:
        database = db
        table_name = 'animals'

    def __str__(self):
        return self.name
    
    def get_animals_by_user_id(user_id):
        return [animal for animal in Animal.select().where(Animal.owner == user_id)]

    def sort_animals(animal_list, sort_by, order):
        if sort_by == 'name':
            if order == 'asc':
                animals = sorted(animal_list, key=lambda animal: animal.name.lower())
            else:
                animals = sorted(animal_list, key=lambda animal: animal.name.lower(), reverse=True)
        elif sort_by == 'species':
            if order == 'asc':
                animals = sorted(animal_list, key=lambda animal: animal.species.lower())
            else:
                animals = sorted(animal_list, key=lambda animal: animal.species.lower(), reverse=True)
        elif sort_by == 'age':
            if order == 'asc':
                animals = sorted(animal_list, key=lambda animal: animal.age)
            else:
                animals = sorted(animal_list, key=lambda animal: animal.age, reverse=True)
        else:
            return animal_list
        
        return animals


class Notes(peewee.Model):
    content = peewee.TextField()
    animal = peewee.ForeignKeyField(Animal, backref='notes')

    class Meta:
        database = db
        table_name = 'notes'

    def __str__(self):
        return self.content
    
    def get_by_animal_id(animal_id):
        return [note for note in Notes.select().where(Notes.animal == animal_id)]

def create_db_tables():
    with db:
        db.create_tables([User, Animal, Notes])

if __name__ == '__main__':
    create_db_tables()
