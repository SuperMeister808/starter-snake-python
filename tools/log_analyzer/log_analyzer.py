import logging
import typing
import os
import json
class LogAnalyzer():

    def __init__(self, file, level_index, turn_index, log_index):
        self.file = file
        self.level_index = level_index
        self.turn_index = turn_index
        self.log_index = log_index
        self.contents = []
        self.logger = None
        self.handlers = {}
        self.setup_logger()

    def setup_logger(self):
        self.logger = logging.getLogger("log_analyzer")
        self.logger.setLevel(logging.INFO)
        
    def setup_handlers(self):
        formatter = self.setup_formatter()
        self.setup_file_handler(self.file, formatter)
        self.setup_stream_handler(formatter)

    def setup_formatter(self):
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - LINE %(line_number)s - TURN %(turn)s - %(message)s", 
                                      datefmt="%Y-%m-%d %H:%M:%S")
        return formatter
    
    def setup_file_handler(self, file, formatter):
        if not isinstance(formatter, logging.Formatter):
            self.close_handlers()
            raise RuntimeError("Formatter object is required to be logging.Formatter()")
        if not os.path.isfile(file):
            self.close_handlers()
            raise RuntimeError("File path does not exist!")

        handler = logging.FileHandler(file)
        handler.setFormatter(formatter)
        self.handlers ["file"] = handler
    
    def setup_stream_handler(self, formatter):
        if not isinstance(formatter, logging.Formatter):
            self.close_handlers()
            raise TypeError("Formatter object is required to be logging.Formatter()")
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.handlers ["console"] = handler

    def add_handler(self, handlers:typing.List[str]):
        for handler_name in handlers:
            handler = self.handlers.get(handler_name, "unknown")
            if not isinstance(handler, logging.Handler):
                self.close_handlers()
                continue
            self.logger.addHandler(handler)

    def remove_handler(self):
        for handler in self.logger.handlers:
            if not isinstance(handler, logging.Handler):
                continue
            self.logger.removeHandler(handler)

    def close_handlers(self):
        self.remove_handler()

        for name, handler in self.handlers.items():
            if isinstance(handler, logging.Handler):
                handler.close()
    
    def read_log(self):
        self.reset_contents()
        if not isinstance(self.file, str):
            self.close_handlers()
            raise RuntimeError(f"Unsupportded file handler")
        try:
            with open(self.file, "r") as f:
                for i, line in enumerate(f):
                    words = line.split("|")
                    content = self.create_contents(words, i, self.level_index, self.turn_index, self.log_index)
                    self.contents.append(content)
            self.save_contents()
        except FileNotFoundError:
            raise RuntimeError("Log file not found!")

    def create_contents(self, words, line_number=None, level_index=None, turn_index=None, log_index=None):
        if line_number is None or not isinstance(line_number, int):
            line_number = "unknown"
        else:
            line_number = line_number
        if level_index is None or level_index > len(words) - 1:
            level = "unknown"
        else:
            raw_level = words[level_index]
            level = raw_level.strip().strip('"').strip("'")
        if turn_index is None or turn_index > len(words) - 1:
            turn = "unknown"
        else:
            raw_turn = words[turn_index]
            for word in raw_turn.split():
                if word.isdigit():
                    turn_string = word
                    turn = int(turn_string)
        if log_index is None or log_index > len(words) - 1:
            log = "unknown"
        else:
            raw_log = words[log_index]
            log = raw_log.strip().strip('"').strip("'")
        content = {"line_number": line_number, "level": level, "turn": turn, "log": log}
        return content
    
    def save_contents(self):
        with open(r"C:\Users\emilc\game_agent\starter-snake-python\tools\log_analyzer\ressources\contents.json", "w") as f:
            contents_json = json.dumps(self.contents)
            f.write(contents_json)

    def load_contents(self):
        with open(r"C:\Users\emilc\game_agent\starter-snake-python\tools\log_analyzer\ressources\contents.json", "r") as f:
            contents_json = f.read()
            contents = json.loads(contents_json)
            try:
                self.validate_contents(contents)
                self.contents = contents
            except RuntimeError:
                self.read_log()
    
    def analyse_errors(self, output_formats):
        if self.contents == {}:
            self.load_contents()
        ALLOWED_OUTPUT_FORMATS = ["file", "console"]
        for output_format in output_formats:
            if output_format not in ALLOWED_OUTPUT_FORMATS:
                self.close_handlers()
                raise RuntimeError(f"Analyse_errors does not accept the output format: {output_format}!")
        if len(self.contents) == 0:
            self.close_handlers()
            raise RuntimeError("Log not read!")
        
        ALLOWED_ERRORS = ["random_choice: Choosed emergency move"]

        for content in self.contents:
            line_number = content.get("line_number", "unknown")
            turn = content.get("turn", "unknown")
            level = content.get("level", "unknown")
            log = content.get("log", "unknown")
            try:
                level_index = self.validate_level(level)
                self.validate_log(log)
            except KeyError as e:
                output = {"line_number": line_number, "level": 40, "turn": turn, "log": f"Line can not be analyzed: {e}"}
                self.output_handler(output_formats, output)
                continue

            if level_index == 40:
                if log not in ALLOWED_ERRORS:
                    output = {"line_number": line_number, "level": level_index, "log": log, "turn": turn}
                    self.output_handler(output_formats, output)

        output = {"line_number": "unknown", "level": 20, "log": "Analyse errors completed!", "turn": "unknown"}
        self.output_handler(output_formats, output)

    def validate_contents(self, contents):
        if not isinstance(contents, list):
            raise RuntimeError("Invalid contents!")
        NEEDED_KEYS = ["line_number", "level", "log", "turn"]
        found_keys = []
        for content in contents:
            for key, value in content.items():
                if key in NEEDED_KEYS:
                    found_keys.append(key)
                else:
                    raise RuntimeError("Invalid contents!")
        if len(found_keys) != len(NEEDED_KEYS):
            raise RuntimeError("Invalid contents!")

    def validate_level(self, level):
        ALLOWED_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level not in ALLOWED_LEVELS:
            raise KeyError("No allowed log leve in contents found")
        level_int = 0
        if level == "DEBUG":
            level_int = 10
        if level == "INFO":
            level_int = 20
        if level == "WARNING":
            level_int = 30
        if level == "ERROR":
            level_int = 40
        if level == "CRITICAL":
            level_int = 50
        return level_int
        
    def validate_log(self, log):
        if log == "unknown":
            raise KeyError("To execute the called analyzation the log neeeds a clear entry!")
        
    def validate_turn(self, turn):
        if not isinstance(turn, int):
            raise KeyError("To execute the called analyzation the log needs clear turns!")
        
    def validate_line_number(self, line_number):
        if not isinstance(line_number, int):
            raise KeyError("To execute called analyzation the log needs clear lines!")

    def output_handler(self, output_handlers, output):
        self.setup_handlers()
        self.add_handler(output_handlers)
        if len(self.logger.handlers) == 0:
            raise RuntimeError("Logger needs one or more handlers!")
        level = output.get("level", 30)
        turn = output.get("turn", "unknown")
        log = output.get("log", "unknown")
        line_number = output.get("line_number", "unknown")
        self.logger.log(level, log, extra={"line_number": line_number, "turn": turn})
        self.close_handlers()
        
    def reset_contents(self):
        self.contents = []