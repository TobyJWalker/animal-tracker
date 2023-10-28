from seeds.seed_db import *

def test_get_animals():
    seed_test_data()

    assert len(Animal.get_animals_by_user_id(1)) == 2