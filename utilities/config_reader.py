import os
import configparser

config = configparser.RawConfigParser()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, "config", "config.ini")

config.read(config_path)


class ReadConfig:

    @staticmethod
    def get_url():
        return config.get('common info', 'baseURL')

    @staticmethod
    def get_username():
        return config.get('common info', 'username')

    @staticmethod
    def get_password():
        return config.get('common info', 'password')
