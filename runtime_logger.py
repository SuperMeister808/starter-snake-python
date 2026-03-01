
import logging
from logging import LoggerAdapter

class RuntimeLogger():

    def __init__(self , logger, file, debug):

        self.setup_logger(logger, debug)
        file_handler = self.create_file_handler(file)
        if isinstance(file_handler, logging.FileHandler):
            self.logger.addHandler(file_handler)
    
    def setup_logger(self, logger, debug):

        self.logger = logging.getLogger(logger)
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        
    def create_file_handler(self, file):
        if not any(isinstance(h, logging.FileHandler) for h in self.logger.handlers):
            file_handler = logging.FileHandler(file, delay=True)
        
            formatter = self.create_runtime_log_formatter()
            file_handler.setFormatter(formatter)
            return file_handler
        
    def create_runtime_log_formatter(self):

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