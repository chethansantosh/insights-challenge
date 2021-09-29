import logging
import os
from datetime import datetime


class Logging:
    def __init__(self, log_file_path):
        """
        :param log_file_path: File path for logging
        """
        self.log_file_path = log_file_path

    def set_logging(self):
        """
        Console and File Handler initialization for logging
        """
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)

        # Console Handler
        log_formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        console_handler.setLevel(logging.INFO)
        log.addHandler(console_handler)

        # File Handler
        log_file_handler = logging.FileHandler(self.log_file_path, 'a')
        log_file_handler.setFormatter(log_formatter)
        log_file_handler.setLevel(logging.DEBUG)
        log.addHandler(log_file_handler)
