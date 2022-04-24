import re
from datetime import date


def get_credentials_from_file(file_name: str) -> str:
    with open(file_name, 'rt', encoding='utf-8') as file:
        return file.read().strip()


def bdate_to_age(birth_date: str) -> int:
    year_of_birth = re.sub(r"\d+\.\d+\.(\d{4})", r"\1", birth_date)
    if year_of_birth != birth_date:
        return date.today().year - int(year_of_birth)
    return None
