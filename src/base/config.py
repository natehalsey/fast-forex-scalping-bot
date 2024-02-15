import logging
import os

from dotenv import load_dotenv


class Config:
    TWS_USERID: str = ""
    TWS_PASSWORD: str = ""
    TRADING_MODE: str = ""
    @classmethod
    def load_from_env(cls):
        for key, value in vars(cls).items():
            if key.isupper() and not key.startswith("__"):
                setattr(cls, key, os.getenv(key, value))

load_dotenv()
Config.load_from_env()
