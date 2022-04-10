from vk.bot import Bot
from utils import get_credentials_from_file


if __name__ == "__main__":
    bot = Bot(
        get_credentials_from_file("credentials/bot_token.txt"),
        get_credentials_from_file("credentials/app_token.txt"),
        'db_user',
        get_credentials_from_file("credentials/db_user_pass.txt")
    )

    bot.run()    