import logging
import typing
import os
import json
from contextlib import contextmanager

# Parses and analyzes Battlesnake log files for critical errors and fallback events.
# Supports multiple output formats and caches parsed contents as JSON.
class LogAnalyzer():

    def __init__(self, file, file_handler, level_index, turn_index, log_index):
        self.file = file
        self.file_handler = file_handler
        self.level_index = level_index
        self.turn_index = turn_index
        self.log_index = log_index
        self.contents = []
        self.logger = None
        self.handlers = {}
        self.setup_logger()

    # Context manager that sets up logging handlers and ensures they are closed afterwards.
    @contextmanager
    def safe_setup_handler(self, setup_handlers):
        try:
            result = setup_handlers()
            yield result
        finally:
            self.close_handlers()
    
    # Initializes the log analyzer logger with INFO level.
    def setup_logger(self):
        self.logger = logging.getLogger("log_analyzer")
        self.logger.setLevel(logging.INFO)
        
    # Sets up all logging handlers with a shared formatter.
    def setup_handlers(self):
        formatter = self.setup_formatter()
        self.setup_file_handler(self.file_handler, formatter)
        self.setup_stream_handler(formatter)

    # Creates a formatter that includes timestamp, level, line number, turn and message.
    def setup_formatter(self):
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - LINE %(line_number)s - TURN %(turn)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        return formatter
    
    # Adds a file handler to the logger using the provided formatter.
    def setup_file_handler(self, file_handler, formatter):
        if not isinstance(formatter, logging.Formatter):
            raise RuntimeError("Formatter must be a logging.Formatter instance")

        handler = logging.FileHandler(file_handler)
        handler.setFormatter(formatter)
        self.handlers["file"] = handler
    
    # Adds a stream handler for console output using the provided formatter.
    def setup_stream_handler(self, formatter):
        if not isinstance(formatter, logging.Formatter):
            raise TypeError("Formatter must be a logging.Formatter instance")

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.handlers["console"] = handler

    # Adds the specified handlers to the logger by name.
    # Silently skips unknown handler names.
    def add_handler(self, handlers: typing.List[str]):
        for handler_name in handlers:
            handler = self.handlers.get(handler_name, "unknown")
            if not isinstance(handler, logging.Handler):
                continue
            self.logger.addHandler(handler)

    # Removes all active handlers from the logger.
    def remove_handler(self):
        for handler in self.logger.handlers:
            if not isinstance(handler, logging.Handler):
                continue
            self.logger.removeHandler(handler)

    # Removes all handlers from the logger and closes them to release file resources.
    def close_handlers(self):
        self.remove_handler()
        for name, handler in self.handlers.items():
            if isinstance(handler, logging.Handler):
                handler.close()
    
    # Reads the log file, parses each line into structured contents and saves them to cache.
    # Lines are split by '|' and mapped to keys using the configured indices.
    def read_log(self):
        self.reset_contents()
        if not isinstance(self.file, str):
            raise RuntimeError("Log file path must be a string")

        try:
            with open(self.file, "r") as f:
                for i, line in enumerate(f):
                    words = line.split("|")
                    content = self.create_contents(words, i, self.level_index, self.turn_index, self.log_index)
                    self.contents.append(content)
            self.save_contents()
        except FileNotFoundError:
            raise RuntimeError("Log file not found!")

    # Parses a single log line into a structured dictionary.
    # Falls back to "unknown" for any field that is missing or invalid.
    def create_contents(self, words, line_number=None, level_index=None, turn_index=None, log_index=None):

        line_number = line_number if isinstance(line_number, int) else "unknown"
        level = self._extract_string(words, level_index)
        turn = self._extract_turn(words, turn_index)
        log = self._extract_string(words, log_index)

        return {"line_number": line_number, "level": level, "turn": turn, "log": log}

    # Extracts and cleans a string value from a word list at the given index.
    # Returns "unknown" if the index is invalid or out of range.
    def _extract_string(self, words, index):
        if index is None or index > len(words) - 1:
            return "unknown"
        try:
            return words[index].strip().strip('"').strip("'")
        except IndexError:
            return "unknown"

    # Extracts the turn number from a word list at the given index.
    # Returns "unknown" if no digit is found or the index is invalid.
    def _extract_turn(self, words, index):
        if index is None or index > len(words) - 1:
            return "unknown"
        try:
            raw_turn = words[index]
            for word in raw_turn.split():
                if word.isdigit():
                    return int(word)
            return "unknown"
        except IndexError:
            return "unknown"
    
    # Saves parsed log contents to the JSON cache for reuse in analysis operations.
    def save_contents(self):
        cache_path = os.path.join(os.path.dirname(__file__), "resources", "contents.json")
        with open(cache_path, "w") as f:
            f.write(json.dumps(self.contents))

    # Loads parsed log contents from the JSON cache.
    # Falls back to re-reading the log file if the cache is invalid.
    def load_contents(self):
        cache_path = os.path.join(os.path.dirname(__file__), "resources", "contents.json")
        with open(cache_path, "r") as f:
            contents = json.loads(f.read())
            try:
                self.validate_contents(contents)
                self.contents = contents
            except RuntimeError:
                self.read_log()
    
    # Scans parsed log contents for critical errors using a whitelist.
    # Outputs results to the specified formats — file, console or both.
    # Level 40 (ERROR) entries not in the whitelist are flagged as critical.
    def analyse_errors(self, output_formats):

        ALLOWED_OUTPUT_FORMATS = ["file", "console"]
        # both entries kept for backward compatibility with logs generated before refactoring
        ALLOWED_ERRORS = ["random_choice: Choosed emergency move", "select_move: Selected emergency move"]

        with self.safe_setup_handler(self.setup_handlers) as _:

            # load contents from cache if not already loaded
            if not self.contents:
                self.load_contents()

            for output_format in output_formats:
                if output_format not in ALLOWED_OUTPUT_FORMATS:
                    raise RuntimeError(f"analyse_errors does not accept output format: {output_format}")

            if not self.contents:
                raise RuntimeError("No log contents found — run read_log first")

            for content in self.contents:
                line_number = content.get("line_number", "unknown")
                turn = content.get("turn", "unknown")
                level = content.get("level", "unknown")
                log = content.get("log", "unknown")

                try:
                    level_index = self.validate_level(level)
                    self.validate_log(log)
                except KeyError as e:
                    # line could not be analyzed — log as warning
                    output = {"line_number": line_number, "level": 30, "turn": turn, "log": f"Line cannot be analyzed: {e}"}
                    self.output_handler(output_formats, output)
                    continue

                # flag ERROR level entries not in the whitelist as critical
                if level_index == 40 and log not in ALLOWED_ERRORS:
                    output = {"line_number": line_number, "level": level_index, "log": log, "turn": turn}
                    self.output_handler(output_formats, output)

            # signal completion
            output = {"line_number": "unknown", "level": 20, "log": "Analyse errors completed!", "turn": "unknown"}
            self.output_handler(output_formats, output)
            self.reset_contents()

    # Validates that contents is a list of dictionaries with the required keys.
    # Raises RuntimeError if the structure is invalid or any key is missing.
    def validate_contents(self, contents):
        if not isinstance(contents, list):
            raise RuntimeError("Invalid contents — expected a list")

        REQUIRED_KEYS = {"line_number", "level", "log", "turn"}

        for content in contents:
            if not isinstance(content, dict):
                raise RuntimeError("Invalid contents — each entry must be a dictionary")
            if set(content.keys()) != REQUIRED_KEYS:
                raise RuntimeError(f"Invalid contents — expected keys {REQUIRED_KEYS}")

    # Validates the log level and returns its integer value.
    # Raises KeyError if the level is not a recognised Python log level.
    def validate_level(self, level):
        LEVEL_MAP = {
            "DEBUG":    10,
            "INFO":     20,
            "WARNING":  30,
            "ERROR":    40,
            "CRITICAL": 50,
        }

        if level not in LEVEL_MAP:
            raise KeyError(f"Unrecognised log level: {level}")

        return LEVEL_MAP[level]
        
    # Validates that the log entry is not unknown before analysis.
    # Raises KeyError if the log could not be parsed from the original line.
    def validate_log(self, log):
        if log == "unknown":
            raise KeyError("Log entry could not be parsed — analysis requires a valid message")
        
    # Validates that the turn is a valid integer before analysis.
    # Raises KeyError if the turn could not be parsed from the original line.
    def validate_turn(self, turn):
        if not isinstance(turn, int):
            raise KeyError("Turn could not be parsed — analysis requires a valid integer")
        
    # Validates that the line number is a valid integer before analysis.
    # Raises KeyError if the line number could not be parsed from the original line.
    def validate_line_number(self, line_number):
        if not isinstance(line_number, int):
            raise KeyError("Line number could not be parsed — analysis requires a valid integer")

    # Routes a log entry to the specified output handlers.
    # Adds handlers before logging and removes them afterwards to avoid duplicate output.
    def output_handler(self, output_handlers, output):
        if not self.logger.handlers:
            raise RuntimeError("Logger requires at least one active handler")
        if not isinstance(output, dict):
            raise RuntimeError("Output must be a dictionary")
        self.add_handler(output_handlers)

        level = output.get("level", 30)
        turn = output.get("turn", "unknown")
        log = output.get("log", "unknown")
        line_number = output.get("line_number", "unknown")

        self.logger.log(level, log, extra={"line_number": line_number, "turn": turn})
        self.remove_handler()
        
    # Resets parsed contents after analysis is complete.
    def reset_contents(self):
        self.contents = []