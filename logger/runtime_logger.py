
import logging
from logging import LoggerAdapter

# Base logger class that sets up and manages the runtime file logger.
# EmergencyLogger builds on this class for async logging support.
class RuntimeLogger:

    @classmethod
    def setup(cls, logger_name, file, debug):
        # creates the logger and attaches a file handler
        logger = cls.create_logger(logger_name, debug)
        cls.add_file_handler(logger, file)

    @classmethod
    def create_logger(cls, logger_name, debug):
        # sets log level to DEBUG if debug mode is enabled, otherwise INFO
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        return logger

    @classmethod
    def add_file_handler(cls, logger, file):
        # only adds a file handler if one doesn't already exist
        if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
            file_handler = logging.FileHandler(file, delay=True)
            file_handler.setFormatter(cls.create_runtime_log_formatter())
            logger.addHandler(file_handler)

    @classmethod
    def create_runtime_log_formatter(cls):
        # formats log entries as "LEVEL | TURN X | message"
        return logging.Formatter("%(levelname)s | TURN %(turn)s | %(message)s")

    @staticmethod
    def close_file_handlers(logger):
        # closes and removes all handlers from the logger after the game ends
        if not isinstance(logger, logging.Logger):
            raise RuntimeError("No logger object provided!")
        try:
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
        except AttributeError:
            raise RuntimeError("No handlers found!")   

# Ensures every log entry has a turn value even if none was provided.
class DefaultTurnAdapter(LoggerAdapter):

    def process(self, msg, **kwargs):
        extra = kwargs.get("extra", {})
        extra.setdefault("turn", "unknown")
        kwargs["extra"] = extra
        return msg, kwargs