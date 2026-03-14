
class LogAnalyzer():

    def __init__(self):
        self.contents = []

    def read_log(self, file, level_index=None, turn_index=None, log_index=None):
        
        if not isinstance(file, str):
            raise RuntimeError(f"Unsupportded file handler")
        with open(file, "r") as f:
            for i, line in enumerate(f):
                words = line.split()
                content = self.create_contents(words, i, level_index, turn_index, log_index)
                self.contents.append(content)

    def create_contents(self, words, line_number=None, level_index=None, turn_index=None, log_index=None):
        if line_number is None or not isinstance(line_number, int):
            line_number = "unknown"
        else:
            line_number = line_number
        if level_index is None or level_index > len(words) - 1:
            level = "unknown"
        else:
            level = words[level_index]
        if turn_index is None or turn_index > len(words) - 1:
            turn = "unknown"
        else:
            turn = words[turn_index]
        if log_index is None or log_index > len(words) - 1:
            log = "unknown"
        else:
            log = words[log_index]
        content = {"line_number": line_number, "level": level, "turn": turn, "log": log}
        return content
    
    def analyse_errors(self, output_format, file_handler=None):

        ALLOWED_OUTPUT_FORMATS = ["file", "console"]
        if output_format not in ALLOWED_OUTPUT_FORMATS:
            raise RuntimeError(f"Analyse_errors does not accept the output format: {output_format}!")
        if len(self.contents) == 0:
            raise RuntimeError("Log not read!")
        
        ALLOWED_ERRORS = ["random_choice: Choosed emergency move"]

        for content in self.contents:
            line_number = content.get("line_number", "unknown")
            level = content.get("level", "unknown")
            log = content.get("log", "unknown")
            try:
                self.validate_level(level)
                self.validate_log(log)
            except KeyError as e:
                output = {"line_number": line_number, "WARNING": "Line can not be analyzed", "exception": e}
                self.output_handler(output_format, output, file_handler)
                continue

            if level == "ERROR":
                if log not in ALLOWED_ERRORS:
                    output = {"line_number": line_number, "level": level, "log": log}
                    self.output_handler(output_format, output, file_handler)

        output = "Analyse_errors complete!"
        self.output_handler(output_format, output, file_handler)

    
    def validate_level(self, level):
        ALLOWED_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level not in ALLOWED_LEVELS:
            raise KeyError("To execute the called analyzation the log needs clear levels!")
        
    def validate_log(self, log):
        if log == "unknown":
            raise KeyError("To execute the called analyzation the log neeeds a clear entry!")
        
    def validate_turn(self, turn):
        if not isinstance(turn, int):
            raise KeyError("To execute the called analyzation the log needs clear turns!")

    def output_handler(self, output_format, output, file_handler=None):
        ALLOWED_OUTPUT_FORMATS = ["file", "console"]
        if output_format not in ALLOWED_OUTPUT_FORMATS:
            raise RuntimeError(f"Log analyzer does not support the output format: {output_format}")
        
        if output_format == "file":
            if isinstance(file_handler, str):
                with open(file_handler, "a") as f:
                    f.write(str(output) + "\n")
            else:
                raise RuntimeError("Unsupported file_handler!")
        if output_format == "console":
            print(output)

    def reset_contents(self):
        self.contents = []