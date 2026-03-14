import io
class LogAnalyzer():

    def __init__(self):
        self.contents = {}

    def read_log(self, file, level_index=None, turn_index=None, log_index=None):
        
        with open(file) as f:
            for i, line in enumerate(f):
                words = []
                for word in line.split():
                    words.append(word)
                content = self.create_contents(words, level_index, turn_index, log_index)
                self.contents [i] = content

    def create_contents(self, words, level_index, turn_index, log_index):
        if level_index is None:
            level = "unknown"
        else:
            level = words[level_index]
        if turn_index is None:
            turn = "unknown"
        else:
            turn = words[turn_index]
        if log_index is None:
            log = "unknown"
        else:
            log = words[log_index]
        content = {"level": level, "turn": turn, "log": log}
        return content
    
    def analyse_errors(self, output_format):

        ALLOWED_OUTPUT_FORMATS = ["file", "console"]
        if output_format not in ALLOWED_OUTPUT_FORMATS:
            raise RuntimeError(f"Analyse_errors does not accept the output format: {output_format}!")
        if self.contents == {}:
            raise RuntimeError("Log not read!")
        
        ALLOWED_ERRORS = ["random_choice: Choosed emergency move"]

        for i , content in self.contents.items():
            level = content.get("level", "unknwon")
            log = content.get("log", "unknwon")
            self.validate_level(level)
            self.validate_log(log)

            if level == "ERROR":
                if log not in ALLOWED_ERRORS:
                    output = {"line_number": i, "level": level, "log": log}
                    self.output_handler(output_format, output)

    
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
            if isinstance(file_handler, io.IOBase):
                with open(file_handler) as f:
                    f.write(output)
        if output_format == "console":
            print(output)