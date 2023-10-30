from lib.models import *
from hashlib import sha256


def seed_test_data():
    # drop existing tables and create new ones
    Notes.drop_table()
    Animal.drop_table()
    User.drop_table()

    # create new tables
    create_db_tables()

    User.create(username='test', email='test@gmail.com', password=sha256('@Test123'.encode()).hexdigest())

    Animal.create(name='ringo', owner=1, species='bird', age=1, date_of_birth='2020-01-01', weight=20.0, height=1.0, length=1.0,)
    Animal.create(name='ralph', owner=1, species='dog', age=10, date_of_birth='2020-01-01', weight=1.0, height=1.0, length=1.0,)

    Notes.create(content='test note 1', animal=1)
    Notes.create(content='test note 2', animal=1)
