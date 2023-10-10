import secrets
import string
import os
import re


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
