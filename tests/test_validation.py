from lib.validation import *
from seeds.seed_db import *

def test_validate_email():
    assert validate_email('test@gmail.com')
    assert validate_email('other@outlook.it')
    assert not validate_email('test@gmail')
    assert not validate_email('test@gmail.')
    assert not validate_email('testgmail.com')

def test_validate_password_length():
    assert validate_password_length('123456')
    assert validate_password_length('12345678')
    assert not validate_password_length('12345')
    assert not validate_password_length('123')

def test_validate_password_capital():
    assert validate_password_capitals('A')
    assert validate_password_capitals('Ab')
    assert not validate_password_capitals('abc')

def test_validate_password_number():
    assert validate_password_number('1')
    assert validate_password_number('a1')
    assert not validate_password_number('a')

def test_validate_password_symbol():
    assert validate_password_symbol('!')
    assert validate_password_symbol('@')
    assert validate_password_symbol('?abc')
    assert validate_password_symbol('abc?')
    assert not validate_password_symbol('abc')

def test_passwords_match():
    assert passwords_match('123', '123')
    assert passwords_match('abc', 'abc')
    assert not passwords_match('abc', '123')
    assert not passwords_match('123', 'abc')

def test_username_already_exists():
    seed_test_data()

    assert check_username_unique('test')
    assert not check_username_unique('test2')

def test_signup_errors():
    expected = {
                'username': [], 
                'email': ['Invalid email address'], 
                'password': ['Password must contain at least one symbol'], 
                'password_rep': ['Passwords do not match']
                }
    assert generate_signup_errors('test', 'test@gmail', 'Abc123', 'abc123') == expected