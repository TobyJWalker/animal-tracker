from seeds.seed_db import *

def test_get_animals():
    seed_test_data()

    assert len(Animal.get_animals_by_user_id(1)) == 2

def test_sort_animals():
    seed_test_data()

    animals = Animal.get_animals_by_user_id(1)

    animals_sorted = Animal.sort_animals(animals, 'name', 'asc')
    assert animals_sorted[0].name == 'ralph'

    animals_sorted = Animal.sort_animals(animals, 'name', 'desc')
    assert animals_sorted[0].name == 'ringo'

    animals_sorted = Animal.sort_animals(animals, 'age', 'asc')
    assert animals_sorted[0].age == 10

    animals_sorted = Animal.sort_animals(animals, 'age', 'desc')
    assert animals_sorted[0].age == 1

    animals_sorted = Animal.sort_animals(animals, 'species', 'asc')
    assert animals_sorted[0].species == 'bird'

    animals_sorted = Animal.sort_animals(animals, 'species', 'desc')
    assert animals_sorted[0].species == 'dog'