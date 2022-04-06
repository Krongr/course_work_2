import re
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from db.db_client import DbClient
from vk_bot import VkBot
from utils import get_credentials_from_file


if __name__ == "__main__":
    
    search_bot_api = VkApi(
        token=get_credentials_from_file("credentials/user_token.txt")
    )
    chat_bot_api = VkApi(
        token=get_credentials_from_file("credentials/bot_token.txt")
    )
    db_client = DbClient(
        user='db_user',
        password=get_credentials_from_file("credentials/db_user_pass.txt")
    )

    search_bot = VkBot(search_bot_api)
    chat_bot = VkBot(chat_bot_api)
    chat_bot_longpoll = VkLongPoll(chat_bot_api)

    for event in chat_bot_longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:

                if event.text == 'ищи':
                    user = search_bot.get_user_info(event.user_id)
                    unwanted_ids = db_client.get_unwanted_ids(event.user_id)
                    if user['age'] == -1:
                        chat_bot.send_message(
                            event.user_id,
                            'напиши свой возраст'
                        )
                    else:
                        candidates = search_bot.get_candidates(
                            user['age'],
                            user['sex'],
                            user['city']
                        )
                        while True:
                            candidate = candidates.pop(0)
                            if chat_bot.check_candidate(
                                candidate,
                                unwanted_ids
                            ):
                                chat_bot.send_photos(
                                    event.user_id,
                                    search_bot.get_photos(candidate['id'])
                                )
                                chat_bot.send_message(
                                    event.user_id,
                                    f'{candidate["first_name"]} '
                                    f'https://vk.com/id{candidate["id"]}'
                                )
                                db_client.create_meeting_list_record(
                                    event.user_id,
                                    candidate["id"]
                                )
                                break                
                
                
                elif (re.match(r'\d+', event.text) != None and
                    event.text == re.match(r'\d+', event.text).group(0)):
                    user['age'] = int(event.text)
                    candidates = search_bot.get_candidates(
                        user['age'],
                        user['sex'],
                        user['city']
                    )
                    while True:
                        candidate = candidates.pop(0)
                        if chat_bot.check_candidate(
                            candidate,
                            unwanted_ids
                        ):
                            chat_bot.send_photos(
                                event.user_id,
                                search_bot.get_photos(candidate['id'])
                            )
                            chat_bot.send_message(
                                event.user_id,
                                f'{candidate["first_name"]} '
                                f'https://vk.com/id{candidate["id"]}'
                            )
                            db_client.create_meeting_list_record(
                                event.user_id,
                                candidate["id"]
                            )
                            break   

                
                elif event.text == 'еще':
                    while True:
                        candidate = candidates.pop(0)
                        if chat_bot.check_candidate(
                            candidate,
                            unwanted_ids
                        ):
                            chat_bot.send_photos(
                                event.user_id,
                                search_bot.get_photos(candidate['id'])
                            )
                            chat_bot.send_message(
                                event.user_id,
                                f'{candidate["first_name"]} '
                                f'https://vk.com/id{candidate["id"]}'
                            )
                            db_client.create_meeting_list_record(
                                event.user_id,
                                candidate["id"]
                            )
                            break
                        

                else:
                    chat_bot.send_message(event.user_id, 'нипанятна')