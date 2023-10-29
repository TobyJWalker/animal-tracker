from seeds.seed_db import *

def test_get_notes():
    seed_test_data()

    notes = Notes.get_by_animal_id(1)

    assert len(notes) == 2