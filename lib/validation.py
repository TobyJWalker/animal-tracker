from re import match
from lib.models import *

def validate_email(email):
    if len(email) > 254:
        return False
    if not match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False
    return True

def validate_password_length(password):
    if len(password) < 6:
        return False
    return True

def validate_password_capitals(password):
    if not match(r'.*[A-Z].*', password):
        return False
    return True

def validate_password_number(password):
    if not match(r'.*[0-9].*', password):
        return False
    return True

def validate_password_symbol(password):
    if not match(r'.*[^a-zA-Z0-9].*', password):
        return False
    return True

def passwords_match(password, password_rep):
    if password != password_rep:
        return False
    return True

def check_username_unique(username):
    try:
        User.get(User.username == username)
        return True
    except:
        return False

def generate_signup_errors(username, email, password, password_conf):
    errors = {
        'username': [],
        'email': [],
        'password': [],
        'password_rep': []
    }

    error_count = 0

    if check_username_unique(username):
        errors['username'].append('Username already exists')
        error_count += 1
    if not validate_email(email):
        errors['email'].append('Invalid email address')
        error_count += 1
    if not validate_password_length(password):
        errors['password'].append('Password must be at least 6 characters long')
        error_count += 1
    if not validate_password_capitals(password):
        errors['password'].append('Password must contain at least one capital letter')
        error_count += 1
    if not validate_password_number(password):
        errors['password'].append('Password must contain at least one number')
        error_count += 1
    if not validate_password_symbol(password):
        errors['password'].append('Password must contain at least one symbol')
        error_count += 1
    if not passwords_match(password, password_conf):
        errors['password_rep'].append('Passwords do not match')
        error_count += 1

    return errors if error_count > 0 else None