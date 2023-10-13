import functools
import secrets
import string
import os
import re
from copy import deepcopy
from flask import request, jsonify
from marshmallow import ValidationError


def is_csv_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == '.csv'

# if is_csv_file(file_path):
#     print(f'The file {file_path} is a CSV file.')
# else:
#     print(f'The file {file_path} is not a CSV file.')


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def convert_numeric_string(value):
    pattern = re.compile(r'(\d+(\.\d+)?)\s*([MmKk]?)')
    match = pattern.match(value)
    if match:
        number_part = float(match.group(1))
        suffix = match.group(3).lower()
        if suffix == 'k':
            number_part *= 1000
        elif suffix == 'm':
            number_part *= 1000000
        return "{:,.0f}".format(number_part)
    return value


def validate_name(name):
    if len(name) < 3:
        raise ValueError("Name must be at least 3 characters long")
    return name


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise ValueError("Invalid email format")
    return email


def validate_request_data(schema, partial=False):
    def validator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            json_data = request.get_json() or dict()
            data = deepcopy(json_data)
            data.update(kwargs)
            try:
                schema.load(data, partial=partial)
            except ValidationError as err:
                return jsonify({"error": str(err)}), 500
            else:
                return func(*args, **kwargs)
        return wrapper
    return validator
