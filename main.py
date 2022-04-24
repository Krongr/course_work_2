import configparser
from vk.bot import Bot


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("settings.ini")
    bot = Bot(
        config['vk']['chat_token'],
        config['vk']['app_token'],
        config['db']['user'],
        config['db']['password']
    )

    bot.run()
