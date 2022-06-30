import logging
import logging.config


def setup_logger(name: str) -> logging.Logger:
    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s', "%m-%d-%Y %H:%M:%S")

    str_formatter = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    logging.basicConfig(filename='work.log',
                        encoding='utf-8',
                        level=logging.DEBUG,
                        format=str_formatter)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # add formatter to ch
    ch.setFormatter(formatter)

    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # add ch to logger
    logger.addHandler(ch)
    return logger
