from random import randrange
from vk_api import VkApi
from utils import  bdate_to_age


class VkBot():
    def __init__(self, api:VkApi):
        self.api = api

    def get_user_info(self, user_id) -> dict:
        params = {
            'user_ids': user_id,
            'fields': 'bdate, sex, city'
        }
        resp = self.api.method('users.get', params)[0]
        return {
            'age': bdate_to_age(resp['bdate']),
            'sex': resp['sex'],
            'city': resp['city']['id'],
        }

    def get_candidates(self, inq_age, inq_sex, inq_city) -> list:
        sex = 1 if inq_sex == 2 else 2
        params = {
                'count': 1000,
                'city': inq_city,
                'sex': sex,
                'age_from': int(inq_age)-5,
                'age_to': int(inq_age)+5,
                'fields': 'bdate, sex, city, relation'
            }
        return self.api.method('users.search', params)['items']

    def check_candidate(self, candidate:dict, unwanted_ids:list) -> bool:
        unwanted_relations = {
            2: 'есть друг/есть подруга',
            3: 'помолвлен/помолвлена',
            4: 'женат/замужем',
            7: 'влюблён/влюблена',
            8: 'в гражданском браке'
        }

        if (
            'relation' in candidate and
            candidate['relation'] in unwanted_relations or
            candidate['id'] in unwanted_ids            
        ):
            return False
        return True

    def get_photos(self, candidate_id:int) -> list:
        params = {
            'user_id': candidate_id,
            'album_id': 'profile',
            'extended': 1
        }
        resp = self.api.method('photos.get', params)['items']
        photos = []
        for photo in resp:
            value = photo['likes']['count'] + photo['comments']['count']
            photos.append({
                'value': value,
                'url': photo['sizes'][-1]['url']
            })
        photos = sorted(photos, key=lambda x: x['value'], reverse=True)
        return photos

    def send_message(self, recipient_id, message) -> None:
        params = {
            'user_id': recipient_id,
            'message': message, 
            'random_id': randrange(10 ** 7)
        }
        self.api.method('messages.send', params)

    def send_photos(self, recipient_id, photos:list) -> None:
        count = 3 if len(photos) >= 3 else len(photos)
        for i in range(count):
            self.send_message(recipient_id, photos[i]['url'])