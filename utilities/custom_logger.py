import logging
import os


class LogGen:

    @staticmethod
    def loggen():

        log_path = "logs/automation.log"

        if not os.path.exists("logs"):
            os.makedirs("logs")

        logger = logging.getLogger("AutomationLogger")
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        file_handler.setFormatter(formatter)

        if not logger.handlers:
            logger.addHandler(file_handler)

        return logger
