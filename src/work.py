from os import system
from time import sleep
from logging import getLogger
from random import randint, uniform
from datetime import datetime, timedelta, date

from psutil import process_iter
from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as MController

from constants import *


class Work:
    logger = getLogger(ROOT)

    def __init__(self) -> None:
        self.keyboard = Controller()
        self.mouse = MController()
        self.keys = [Key.caps_lock,
                     Key.ctrl_l,
                     Key.ctrl_r,
                     Key.alt_l,
                     Key.alt_r,
                     Key.shift_l,
                     Key.shift_r]

    def sleep_r(self) -> None:
        """Sleeps for a random amount of time 1-30 seconds"""
        sleep_time = randint(1, 30)
        self.logger.debug(f"Sleeping {sleep_time} seconds\n")
        sleep(sleep_time)

    def keyboard_move(self) -> None:
        """Randomly presses a key on the keyboard within the specified options list."""
        k_choice = randint(0, len(self.keys)-1)
        self.keyboard.tap(self.keys[k_choice])
        self.logger.debug(self.keys[k_choice])

        if self.keys[k_choice] == Key.caps_lock:
            sleep(1)
            self.keyboard.tap(Key.caps_lock)

    def mouse_move(self) -> None:
        """Moves mouse to set (x, y) position"""
        x = randint(-60, 60)
        y = randint(-60, 60)
        num_loops = min(abs(x), abs(y))
        m_sleep_time = uniform(0.001, 0.01)

        # move mouse relative to current position
        for _ in range(num_loops):
            self.mouse.move(x, y)
            self.logger.debug(f"Mouse position: {self.mouse.position}")
            sleep(m_sleep_time)
        sleep(1)

    def kill_process(self, process_name: str) -> None:
        """Kill the running process"""
        self.logger.debug(f"Killing process {process_name}")
        result = system(f"taskkill /f /im {process_name}")
        if result == -1:
            self.logger.debug(f"Failed to stop process {process_name}")
        else:
            self.logger.debug(f"Successfully killed process {process_name}")

    def activate_process(self, process_name: str) -> None:
        self.logger.debug(f"Activating process {process_name}")
        cmd = f"AppData/Local/Microsoft/Teams/Update.exe --processStart {process_name}"
        self.logger.debug(cmd)
        result = system(cmd)

        if result == -1:
            self.logger.debug(f"Activation of {process_name} failed")
        else:
            self.logger.debug(f"Activation of {process_name} successful")

    def is_process_active(self, process_name: str) -> bool:
        for proc in process_iter():
            if proc.name() == process_name:
                # process is active
                return True
        return False

    def is_work_time(self) -> bool:
        """Returns true if the current time is between the hours of 10:00AM - 6:00PM"""
        start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        end_time = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
        current_time = datetime.now().replace(second=0, microsecond=0)
        return current_time >= start_time and current_time < end_time

    def get_remaining_time_until_work(self) -> timedelta:
        current_time = datetime.now().replace(second=0, microsecond=0)
        today = date.today()
        start_time = datetime(
            year=today.year, month=today.month, day=today.day, hour=10)

        if current_time.hour > 10:
            start_time += timedelta(days=1, hours=0)

        time_left = timedelta(days=start_time.day, hours=start_time.hour, minutes=start_time.minute) - \
            timedelta(days=current_time.day, hours=current_time.hour,
                      minutes=current_time.minute)
        return time_left

    def work_loop(self) -> None:
        while True:
            self.mouse_move()
            self.keyboard_move()

            if not self.is_work_time():
                time_left = self.get_remaining_time_until_work()
                hours     = round((time_left.total_seconds() // 60) // 60)
                minutes   = round((time_left.total_seconds() // 60) - (hours * 60))
                self.logger.debug(f"{hours} hours and {minutes} minutes until work time")

                if self.is_process_active(TEAMS):
                    self.kill_process(TEAMS)

                sleep_time = 60
                self.logger.debug(f"Sleeping for {sleep_time // 60} minute")
                sleep(sleep_time)
                continue

            # It's work time!
            if not self.is_process_active(TEAMS):
                self.activate_process(TEAMS)

            self.sleep_r()
