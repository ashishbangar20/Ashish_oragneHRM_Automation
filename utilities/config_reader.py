import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class ReadConfig:

    @staticmethod
    def get_url():
        return os.getenv("BASE_URL")

    @staticmethod
    def get_username():
        return os.getenv("USERNAME")

    @staticmethod
    def get_password():
        return os.getenv("PASSWORD")

