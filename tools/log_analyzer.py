class LogAnalyzer():

    def __init__(self):
        self.ALLOWED_ERRORS = [
           "random_choice: Choosed emergency move"
        ]
        self.contents = {}

    def read_log(self, file):
        
        with open(file) as f:
            for i, line in enumerate(f):
                words = []
                for word in line.split():
                    words.append(word)
                level = words[0]
                turn = word[2]
                log = word[-1]
                content = {"level": level, "turn": turn, "log": log}
                self.contents [i] = content

    def analyse_errors(self, line, line_number, file=None):
        
        ALLOWED_ERRORS = ["random_choice: Choosed emergency move"]
        if self.contents == {}:
            try:
                self.read_log(file)
            except Exception:
                raise RuntimeError("Log not read!")

        for i , content in self.contents.items():
            level = content.get("level", "unknwon")
            turn = content.get("turn", "unknwon")
            log = content.get("log", "unknwon")

        self.validate_level(level)

        if level == "ERROR":
            pass
    
    def validate_level(self, level):
        ALLOWED_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level not in ALLOWED_LEVELS:
            raise KeyError("To execute the called analyzation the log needs clear levels!")
        
    def validate_log(self, log):
        if log == "unknown":
            raise KeyError("To execute the called analyzation the log neeeds a clear entry!")

    def print_found_errors(self, found_errors):
        for error in found_errors:
            print(error)