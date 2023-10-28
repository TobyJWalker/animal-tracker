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
