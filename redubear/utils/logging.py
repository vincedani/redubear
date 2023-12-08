# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import logging


def get_logger(name: str, log_level: int = logging.getLogger().level):
    logger = logging.getLogger(name)

    # Already initialized logger.
    if logger.handlers:
        return logger

    if isinstance(log_level, str):
        log_level = logging.getLevelName(log_level)

    logging.basicConfig(level=log_level)
    logger.setLevel(log_level)
    logger.propagate = False

    # Logging to the console.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(StreamFormatter())
    logger.addHandler(console_handler)

    return logger


class StreamFormatter(logging.Formatter):
    green = "\x1b[32m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    message_format = "%(message)s"

    FORMATS = {
        logging.DEBUG: green + message_format + reset,
        logging.INFO: green + message_format + reset,
        logging.WARNING: yellow + message_format + reset,
        logging.ERROR: red + message_format + reset,
        logging.CRITICAL: bold_red + message_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)

        formatter = logging.Formatter(log_fmt)
        formatted = formatter.format(record)

        return f'{formatted}'
