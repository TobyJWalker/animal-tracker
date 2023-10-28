from seeds.seed_db import *

def test_check_login():
    seed_test_data()

    assert User.check_login('test', '@Test123')
    assert not User.check_login('test', 'abc123')
    assert not User.check_login('test', 'Abc1234')
    assert not User.check_login('test2', '@Test123')