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
    
    def analyse_errors(self):
        
        ALLOWED_ERRORS = ["random_choice: Choosed emergency move"]
        if self.contents == {}:
            raise RuntimeError("Log not read!")

        for i , content in self.contents.items():
            level = content.get("level", "unknwon")
            log = content.get("log", "unknwon")
            self.validate_level(level)
            self.validate_log(log)

        if level == "ERROR":
            pass
    
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

    def print_found_errors(self, found_errors):
        for error in found_errors:
            print(error)