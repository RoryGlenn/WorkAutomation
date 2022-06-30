"""main.py - entry point for program"""

# from threading import Thread
from constants import ROOT

from work import Work
from coms import Coms
from log import setup_logger


def main() -> None:
    """Entry point for program"""

    logger = setup_logger(ROOT)
    logger.debug("Starting...")

    work = Work()
    coms = Coms()

    # cm_thread = Thread(target=coms.check_messages_t)
    # cm_thread.start()

    # start the work loop
    work.work_loop()

    # kill the thread and end the program
    coms.set_thread_activity(False)
    # cm_thread.join()

    # for testing only
    # coms.text_phone()


if __name__ == '__main__':
    # system('cls')
    main()


