from constants import ROOT
from time import sleep
from os import SEEK_END
from config import Config
from io import TextIOWrapper
from typing import Generator
from logging import getLogger
from twilio.rest import Client
from constants import NEW_ACTIVITY, TEAMS_LOG_FILE


logger = getLogger(ROOT)


class Coms:
    def __init__(self) -> None:
        self.thread_status = True
        self.config = Config()
        self.t_client = Client(username=self.config.username,
                               password=self.config.password,
                               account_sid=self.config.account_sid)

    def text_phone(self) -> None:
        """Text cell phone upon a new message in Teams"""
        try:
            message = self.t_client.messages.create(
                to=self.config.phone_number,
                from_=self.config.twilio_phone_number,
                body='Someone messaged you on Teams!')
            logger.debug(f"Texted phone, message id: {message.sid}")
        except Exception as e:
            logger.exception(e)

    def teams_message(self, log_lines: Generator) -> None:
        """If there is a new activity detected in the teams log file, check if it is a new message."""
        for line in log_lines:
            if NEW_ACTIVITY in line:
                logger.debug(line)
                self.text_phone()

    def set_thread_activity(self, status: bool) -> None:
        self.thread_status = status

    def follow(self, log_file: TextIOWrapper) -> Generator:
        """Return the newest line entered at the end of the text file"""
        log_file.seek(0, SEEK_END)

        while True:
            line = log_file.readline()

            if not self.thread_status:
                logger.debug('Ending follow thread')
                break
            if not line:
                sleep(1)
                continue
            yield line

    def check_messages_t(self) -> None:
        """Constantly checks for new messages in Teams"""
        log_file = open(TEAMS_LOG_FILE)
        log_lines = self.follow(log_file)
        self.teams_message(log_lines)
        log_file.close()
