from lib.models import *

def test_create_db_tables():
    create_db_tables()
    assert User.table_exists() == True
    assert Animal.table_exists() == True
    assert Notes.table_exists() == True