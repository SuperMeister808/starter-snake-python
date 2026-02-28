
import logging
from logging import LoggerAdapter

class RuntimeLogger():

    def __init__(self , file, debug):

        self.logger = self.setup_logger(debug)
        file_handler = self.create_file_handler(file)
        self.logger.addHandler(file_handler)
    
    def setup_logger(self, debug):

        logger = logging.getLogger("RuntimeLogger")
        if debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        return logger
        
    def create_file_handler(self, file):
        file_handler = logging.FileHandler(file, delay=True)
        
        formatter = self.create_runtime_log_formatter()
        file_handler.setFormatter(formatter)
        return file_handler
        
    def create_runtime_log_formatter(self):

        formatter = logging.Formatter(
            "%(levelname)s | TURN %(turn)s | %(message)s"
        )
        return formatter
    
    def create_runtime_logger(self):

        return self.logger
    
class DefaultTurnAdapter(LoggerAdapter):

    def process(self, msg, **kwargs):

        extra = kwargs.get("extra", {})
        extra.setdefault("turn", "unknown")
        kwargs["extra"] = extra
        return msg , kwargs