import os
import sys
sys.path.append(os.getcwd())

from random import randrange
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from app_user import AppUser
from db.db_client import DbClient

from utils import get_credentials_from_file


class Bot():
    def __init__(self, chat_token, app_token, db_user, db_pass):
        self.chat = VkApi(token=chat_token)
        self.longpoll = VkLongPoll(self.chat)
        self.app = VkApi(token=app_token)
        self.db_client = DbClient(db_user, db_pass)
        self.users = {}


    def get_user_info(self, id:int) -> dict:
        params = {
            'user_ids': id,
            'fields': 'bdate, sex, city'
        }
        return self.app.method('users.get', params)[0]

    def search_for_candidates(self, user:AppUser) -> list:
        sex = 1 if user.sex == 2 else 2
        params = {
                'count': 1000,
                'city': user.city,
                'sex': sex,
                'age_from': int(user.age)-5,
                'age_to': int(user.age)+5,
                'fields': 'bdate, sex, city, relation, is_closed'
            }
        return self.app.method('users.search', params)['items']

    def get_photos(self, id:int) -> list:
        params = {
            'user_id': id,
            'album_id': 'profile',
            'extended': 1
        }
        resp = self.app.method('photos.get', params)['items']
        photos = []
        for photo in resp:
            value = photo['likes']['count'] + photo['comments']['count']
            photos.append({
                'value': value,
                'url': photo['sizes'][-1]['url']
            })
        photos = sorted(photos, key=lambda x: x['value'], reverse=True)
        return photos

    def send_photos(self, recipient_id, candidate_id) -> None:
        photos = self.get_photos(candidate_id)
        count = 3 if len(photos) >= 3 else len(photos)
        for i in range(count):
            self.send_message(recipient_id, photos[i]['url'])

    def check_candidate(self, user:int, candidate:dict) -> bool:
        unwanted_relations = {
            2: 'есть друг/есть подруга',
            3: 'помолвлен/помолвлена',
            4: 'женат/замужем',
            7: 'влюблён/влюблена',
            8: 'в гражданском браке'
        }
        if candidate['is_closed']:
            return False
        unwanted_ids = self.db_client.get_unwanted_ids(user)
        if (
            'relation' in candidate and
            candidate['relation'] in unwanted_relations or
            candidate['id'] in unwanted_ids            
        ):
            return False
        return True

    def send_message(self, recipient_id, message) -> None:
        params = {
            'user_id': recipient_id,
            'message': message, 
            'random_id': randrange(10 ** 7)
        }
        self.chat.method('messages.send', params)


    def get_started(self, event) -> None:
        self.users[event.user_id] = AppUser(self.get_user_info(event.user_id))

        if self.users[event.user_id].age == None:
            self.send_message(event.user_id, "Введите свой возраст")
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        try:
                            self.users[event.user_id].fill_age(
                                int(event.text)
                            )
                            break
                        except ValueError:
                            self.send_message(
                                event.user_id, "Введите свой возраст"
                            )

        if self.users[event.user_id].city == None:
            self.send_message(event.user_id, "Введите название своего города")
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        city_id = self.app.method(
                            'database.getCities',
                            {
                                'country_id': 1,
                                'q': event.text,
                                'count': 1
                            }
                        )['items'][0]['id']
                        self.users[event.user_id].fill_city(city_id)
                        break

        self.users[event.user_id].add_candidates(
            self.search_for_candidates(self.users[event.user_id])
        )
        self.send_message(
            event.user_id,
            'Привет! Я готов. Для поиска отправь: "искать".'
        )

    def send_candidat(self, event) -> None:
        while True:
           candidate = self.users[event.user_id].candidates.pop(0)
           if self.check_candidate(event.user_id, candidate):
               self.send_message(
                   event.user_id,
                   f'{candidate["first_name"]} '
                   f'https://vk.com/id{candidate["id"]}'
                )
               self.send_photos(event.user_id, candidate['id'])
               self.db_client.create_meeting_list_record(
                   event.user_id,
                   candidate['id']
               )
               break

    def block_candidat(self, event) -> None:
        pass
    
    def send_help(self, event) -> None:
        self.send_message(
            event.user_id,
            """Для начала работы отправь "привет",
            для поиска кандидатов - "искать",
            для блокировки кандидата - "заблокировать".            
            """
        )

    def run(self) -> None:
        commands = {
            'привет': self.get_started,
            'искать': self.send_candidat,
            'заблокировать': self.block_candidat
        }

        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    try:
                        commands[event.text](event)
                    except KeyError:
                        self.send_help(event)

bot = Bot(
    get_credentials_from_file("credentials/bot_token.txt"),
    get_credentials_from_file("credentials/app_token.txt"),
    'db_user',
    get_credentials_from_file("credentials/db_user_pass.txt")
)

bot.run()