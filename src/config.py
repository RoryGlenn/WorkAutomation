from json import load
from os import path
from sys import exit as sys_exit

from constants import *

from logging import getLogger


logger = getLogger(ROOT)


class Config:
    def __init__(self) -> None:
        self.account_sid = None
        self.auth_token = None
        self.twilio_phonep_number = None
        self.phone_number = None
        self.username = None
        self.password = None
        self.__post_init()

    def __get_config(self) -> dict:
        """Returns config file as a dictionary"""
        if path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                return load(file)

        logger.debug("config.json file not found")
        sys_exit(1)

    def __set_variables(self, config: dict) -> None:
        self.account_sid = config['account_sid']
        self.auth_token = config['auth_token']
        self.twilio_phone_number = config['twilio_phone_number']
        self.phone_number = config['phone_number']
        self.username = config['username']
        self.password = config['password']

    def __post_init(self) -> None:
        config = self.__get_config()
        self.__set_variables(config)
