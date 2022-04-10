import os
import sys
sys.path.append(os.getcwd())

from utils import bdate_to_age


class AppUser():
    def __init__(self, users_get_resp:dict) -> None:
        self.id = users_get_resp['id']
        try:
            self.age = bdate_to_age(users_get_resp['bdate'])
        except KeyError:
            self.age = None
        self.sex = users_get_resp['sex']
        try:        
            self.city = users_get_resp['city']['id']
        except KeyError:
            self.city = None
        self.candidates = []

    def fill_age(self, age:int) -> None:
        self.age = age

    def fill_city(self, city:int) -> None:
        self.city = city

    def add_candidates(self, candidates:list) -> None:
        self.candidates += candidates