
import logging
from logging import LoggerAdapter

class RuntimeLogger():

    @classmethod
    def setup(cls, logger_name, file, debug):
        logger = cls.create_logger(logger_name, debug)
        cls.add_file_handler(logger, file)
    
    @classmethod
    def create_logger(cls, logger, debug):

        logger = logging.getLogger(logger)
        if debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        return logger

    @classmethod
    def add_file_handler(cls, logger, file):
        if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
            file_handler = logging.FileHandler(file, delay=True)
        
            formatter = cls.create_runtime_log_formatter()
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
    @classmethod
    def create_runtime_log_formatter(cls):

        formatter = logging.Formatter(
            "%(levelname)s | TURN %(turn)s | %(message)s"
        )
        return formatter
    
    @staticmethod
    def close_file_handlers(logger):
        if not isinstance(logger, logging.Logger):
            raise RuntimeError("Kein logger Objekt übergeben!")
        
        try:
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
        except AttributeError:
            raise RuntimeError("Keine Handler vorhanden!")    

class DefaultTurnAdapter(LoggerAdapter):

    def process(self, msg, **kwargs):

        extra = kwargs.get("extra", {})
        extra.setdefault("turn", "unknown")
        kwargs["extra"] = extra
        return msg , kwargs